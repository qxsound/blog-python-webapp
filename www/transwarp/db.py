#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time, uuid, threading, logging

# 数据库引擎对象
class _Engine(object):
	def __init__(self, connect):
		self._connect = connect

	def connect(self):
		return self._connect()  #因为传入的是lambda表达式，所以是个函数，要加括号

class DBError(Exception):
	pass

class MultiColumnsError(DBError):
	pass

class Dict(dict):
	'''
	能支持 x.y 形式的dict,不需要每次都写x[y]
	'''
	def __init__(self, names=(), values=(), **kw):
		super(Dict, self).__init__(**kw)
		for k, v in zip(names, values):
			self[k] = v

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value



def next_id(t=None):
	'''
	return next id as 50-char string.

	参数:
		t 默认是none，用的是时间戳 time.time()
	'''
	if t is None:
		t = time.time()
	return '%015d%s000' % (int(t * 1000), uuid.uuid4().hex)

def _profiling(start, sql=''):
	t = time.time() - start
	if t > 0.1:
		logging.warning('[PROFILING] [DB] %s: %s' % (t, sql))
	else:
		logging.info('[PROFIlING] [DB] %s: %s' % (t, sql))

# global engine object
engine = None

def create_engine(user, password, database, host='127.0.0.1', port=3306, **kw):
	import mysql.connector
	global engine
	if engine is not None:
		raise DBError('Engine is already initialized...')
	params = dict(user=user, password=password, database=database, host=host, port=port)
	defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci',autocommit=False)
	for k,v in defaults.iteritems():
		params[k] = kw.pop(k, v)
	params.update(kw)
	params['buffered'] = True
	engine = _Engine(lambda: mysql.connector.connect(**params))
	# test connection...
	logging.info('Init mysql engine <%s> complete...' % hex(id(engine)))


class _LazyConnection(object):
	def __init__(self):
		self.connection = None

	def cursor(self):
		if self.connection is None:
			self.connection = engine.connect()
			logging.info('open connection %s...' % hex(id(connection)))
		return self.connection.cursor()

	def commit(self):
		self.connection.commit()

	def rollback(self):
		self.connection.rollback()

	def cleanup(self):
		if self.connection:
			self.connection.close()
			self.connection = None
			logging.info('close connection %s...' % hex(id(connection)))


# 持有数据库连接的上下文对象
class _DbCtx(threading.local):
	def __init__(self):
		self.connection = None
		self.transactions = 0

	def init(self):
		self.connection = _LazyConnection()
		self.transactions = 0

	def is_init(self):
		return not self.connection == None

	def cleanup(self):
		self.connection.cleanup()
		self.transactions = None

	def cursor(self):
		return self.connection.cursor()

_db_ctx = _DbCtx()

class _ConnectionCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_cleanup = False	
		if not _db_ctx.is_init():
			_db_ctx.init()
			self.should_cleanup = True
		return self

	def __exit__(self, exctype, excvalue, traceback):
		global _db_ctx
		if self.should_cleanup:
			_db_ctx.cleanup()

def connection():
	return _ConnectionCtx()	

import functools
# 用装饰器来实现批量操作
def with_connection(func):
	@functools.wraps(func)
	def wrapper(*args, **kw):
		with _ConnectionCtx():
			return func(*args, **kw)
	return wrapper


class _TransactionCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_close_conn = False
		if not _db_ctx.is_init():
			_db_ctx.init
			self.should_close_conn = True
			_db_ctx.transactions += 1
		return self

	def __exit__(self, exctype, excvalue, traceback):
		global _db_ctx
		_db_ctx.transactions -= 1
		try:
			if _db_ctx == 0:
				if exctype is None: #这里是不是非空？写反了？
					return self.commit()
				else:
					self.rollback()
		finally:
			if self.should_close_conn:
				_db_ctx.cleanup()

	def commit(self):
		global _db_ctx
		try:
			_db_ctx.connection.commit()
		except:
			_db_ctx.rollback()
			raise
	def rollback(self):
		global _db_ctx
		_db_ctx.connection.rollback()

def transaction():
	return _TransactionCtx()

def with_transaction(func):
	@functools.wraps(func)
	def wrapper(*args, **kw):
		_start = time.time()
		with _TransactionCtx():
			return func(*args, **kw)
		_profiling(_start)
	return wrapper

def _select(sql, first, *args):
	'执行查询语句，并返回查询结果 或者是 list形式的结果'
	global _db_ctx
	cursor = None
	sql = sql.replace('?', '%s')
	logging.info('SQL:%s, ARGS:%s' % (sql, args))
	try:
		cursor = _db_ctx.connection.cursor()
		cursor.execute(sql, args)
		if cursor.description:
			names = [x[0] for x in cursor.description]
		if first:
			values = cursor.fetchone()
			if not values:
				return None
			return Dict(names, values)
		return [Dict(names, x) for x in cursor.fetchall()]
	finally:
		if cursor:
			cursor.close()

@with_connection
def select_one(sql, *args):
	'''
	查询一条结果
	'''
	return _select(sql, True, *args)


@with_connection
def select_int(sql, *args):
	'''
	查询一个类型为int的结果
	'''
	d = _select(sql, True, *args)
	if len(d) != 1:
		raise MultiColumnsError('Expect only one column.')
	return d.values()[0]


@with_connection
def select(sql, *args):
	return _select(sql, False, *args)


@with_connection
def _update(sql, *args):
	global _db_ctx
	cursor = None
	sql = sql.replace('?', '%s')
	logging.info('SQL: %s, ARGS: %s' %(sql, args))
	try:
		cursor = _db_ctx.connection.cursor()
		cursor.execute(sql, args)
		r = cursor.rowcount
		if _db_ctx.transactions==0:
			logging.info('auto commit')
			_db_ctx.connection.commit()
		return r
	finally:
		if cursor:
			cursor.close()		

def insert(table, **kw):
	cols, args = zip(**kw.iteritems())
	sql = 'insert into "%s" (%s) values (%s)' % (table, ','.join(['"%s"' % col for col in cols]), ','.join(['?' for i in range(len(cols))]))
	return _update(sql, *args)


def update(sql, *args):
	return _update(sql, *args)

if __name__=='__main__':
	logging.basicConfig(level=logging.DEBUG)
	create_engine('root', 'abcd', 'test')
	update('drop table if exists user')
	update('create table user (id int primary key, name text, email text, passwd text, last_modified real)')
	import doctest
	doctest.testmod()




