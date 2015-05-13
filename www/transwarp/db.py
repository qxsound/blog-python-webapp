# db.py
#!/usr/bin/env python
# -*-coding:utf8-*-

import time, uuid, threading, logging

# 数据库引擎对象
class _Engine(object):
	def __init__(self, connect):
		self._connect = connect

	def connect(self):
		return self._connect

engine = None

class _lazyConnection(object):
	def __init__(self):
		self.connection = None

	def cursor(self):
		if self.connection is None:
			self.connection = engine.connect()
			logging.info('open connection %s...' % hex(id(connection)))
			self.connection = connection
		return self.connection.cursor()

	def commit(self):
		self.connection.commit()

	def rollback(self):
		self.connection.rollback()

	def cleanup(self):
		if self.connection:
			self.connection.close()
			self.connection = None

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
		if not _db_ctx.is_init:
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
		global _db_ctx
		should_cleanup = False	
		if not _db_ctx.is_init:
			_db_ctx.init()
			should_cleanup = True

		func(*args, **kw)

		if should_cleanup:
			_db_ctx.cleanup()
	return wrapper


class _TransactionCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_close_conn = False
		if not _db_ctx.is_init:
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