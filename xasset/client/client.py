#!/usr/bin python3
# -*- coding: utf-8 -*-
# @file       : client.py
# @create time: 2022/05/20
# @说明       : 本文件实现了请求xasset-ui的逻辑

import os, sys

from numpy import True_, int64, isin
sys.path.append(os.getcwd())

import json
from xasset.client.conn import Conn
from xasset.client.param import Param
from xasset.utils.utils import Utils
from xasset.auth.account import XassetAccount

# 主要URI参数
# 浏览器数据
Browser_Srdscir_URI = '/xasset/browser/v1/srdscir'
Browser_QueryAsset_URI =  '/xasset/browser/v1/queryasset'

# 主要资产操作
QueryAsset_URI =  '/xasset/horae/v1/query'
CreateAsset_URI = '/xasset/horae/v1/create'
AlterAsset_URI = '/xasset/horae/v1/alter'
PublishAsset_URI = '/xasset/horae/v1/publish'
GrantAsset_URI =  '/xasset/horae/v1/grant'
QueryShard_URI = '/xasset/horae/v1/querysds'
TransferShard_URI =  '/xasset/damocles/v1/transfer'
FreezeAsset_URI =  '/xasset/horae/v1/freeze'
ConsumeShard_URI = '/xasset/horae/v1/consume'
ListAstByAddr_URI = '/xasset/horae/v1/listastbyaddr'
ListSrdsByAddr_URI = '/xasset/horae/v1/listsdsbyaddr'
ListSrdsByAst_URI = '/xasset/horae/v1/listsdsbyast'
History_URI = '/xasset/horae/v1/history'

class Client(object):
    def browser_srdscir(self, asset_id):
        data = {}
        data['asset_id'] = asset_id
        return self._conn.post(Browser_Srdscir_URI, data)

    def browser_query_asset(self, asset_id, page, limit):
        data = {}
        data['asset_id'] = asset_id
        data['page'] = page
        data['limit'] = limit
        return self._conn.post(Browser_QueryAsset_URI, data)

    def query_asset(self, asset_id):
        data = {
            'asset_id': asset_id,
        }
        resp = self._conn.sign_post(QueryAsset_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("query succ. resp: %s" % resp)
        return resp['meta']

    def create_asset(self, param):
        if not Param.create_asset_valid(param):
            print("create param invalid, param: %s" % param)
            return None

        asset_id = Utils.gen_asset_id(self._conn.app_id())
        data = Param.sign_msg(asset_id, param['account'])
       
        data['asset_info'] = json.dumps(param['asset_info'])
        data['asset_id'] = asset_id
        data['price'] = param['price']
        data['amount'] = param['amount']
        if 'user_id' in param.keys():
            data['user_id'] = param['user_id']

        resp = self._conn.sign_post(CreateAsset_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("server return error no, resp: %s" % resp)
            return None
        print("create succ. resp: %s" % resp)
        return resp['asset_id']

    def alter_asset(self, param):
        if not Param.alter_valid(param):
            print("alter param invalid, param: %s" % param)
            return None
        
        data = Param.sign_msg(param['asset_id'], param['account'])
        data['asset_id'] = param['asset_id']
        if 'amount' in param.keys():
            data['amount'] = param['amount']
        if 'price' in param.keys():
            data['price'] = param['price']
        if 'asset_info' in param.keys():
            data['asset_info'] = json.dumps(param['asset_info'])
        if 'file_hash' in param.keys():
            data['file_hash'] = param['file_hash']

        resp = self._conn.sign_post(AlterAsset_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("alter succ. resp: %s" % resp)
        return 0

    def publish_asset(self, param):
        if not Param.publish_valid(param):
            print("publish param invalid, param: %s" % param)
            return None

        asset_id = param['asset_id']
        data = Param.sign_msg(asset_id, param['account'])
       
        data['asset_id'] = asset_id
        if 'is_evidence' in param.keys():
            data['is_evidence'] = param['is_evidence']
        
        resp = self._conn.sign_post(PublishAsset_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("publish succ. resp: %s" % resp)
        return 0

    def grant_shard(self, param):
        if not Param.grant_valid(param):
            print("grant param invalid, param: %s" % param)
            return None

        asset_id = param['asset_id']
        data = Param.sign_msg(asset_id, param['account'])

        data['asset_id'] = param['asset_id']
        if 'shard_id' in param.keys():
            data['shard_id'] = param['shard_id']
        else:
            data['shard_id'] = Utils.gen_nonce()

        data['to_addr'] = param['to_addr']

        if 'price' in param.keys():
            data['price'] = param['price']
        if 'to_userid' in param.keys():
            data['to_userid'] = param['to_userid']

        resp = self._conn.sign_post(GrantAsset_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("grant succ. resp: %s" % resp)
        return resp

    def query_shard(self, param):
        if not Param.query_shard_valid(param):
            print("query param invalid, param: %s" % param)
            return None

        data = {
            'asset_id': param['asset_id'],
            'shard_id': param['shard_id'],
        }
        resp = self._conn.sign_post(QueryShard_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("query shard succ. resp: %s" % resp)
        return resp['meta']

    def transfer_shard(self, param):
        if not Param.transfer_valid(param):
            print("transfer param invalid, param: %s" % param)
            return None

        data = Param.sign_msg(param['asset_id'], param['account'])
        data['asset_id'] = param['asset_id']
        data['shard_id'] = param['shard_id']
        data['to_addr'] = param['to_addr']
        if 'price' in param.keys():
            data['price'] = param['price']
        if 'to_userid' in param.keys():
            data['to_userid'] = param['to_userid']

        resp = self._conn.sign_post(TransferShard_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("transfer succ. resp: %s" % resp)
        return 0

    def freeze_asset(self, param):
        if not Param.freeze_valid(param):
            print("freeze param invalid, param: %s" % param)
            return False
        
        asset_id = param['asset_id']
        data = Param.sign_msg(asset_id, param['account'])
        data['asset_id'] = '%d' % asset_id
    
        resp = self._conn.sign_post(FreezeAsset_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("freeze succ. resp: %s" % resp)
        return 0

    def consume_shard(self, param):
        if not Param.consume_valid(param):
            print("consume param invalid, param: %s" % param)
            return False

        create_account_json = param['create_account']
        create_addr = create_account_json['addr']
        create_sk = create_account_json['sk']
        create_account = XassetAccount(create_addr, create_sk)
        signMsg = '%d%d' % (param['asset_id'], param['nonce'])
        create_sign = create_account.sign_ecdsa(signMsg)
        data = {
            'asset_id': param['asset_id'],
            'shard_id': param['shard_id'],
            'nonce': param['nonce'],
            'addr': create_addr,
            'pkey': create_account.public_key(),
            'sign': create_sign,
            'user_addr': param['user_addr'],
            'user_sign': param['user_sign'],
            'user_pkey': param['user_pkey'],
        }
        
        resp = self._conn.sign_post(ConsumeShard_URI, data)
        if 'errno' not in resp.keys():
            print("panic, resp: %s" % resp)
            return None
        if resp['errno'] != 0:
            print("error, resp: %s" % resp)
            return None
        print("consume shard succ. resp: %s" % resp)
        return 0
    
    def list_asset_by_addr(self, param):
        return None

    def list_shards_by_addr(self, param):
        return None
    
    def list_shards_by_asset(self, param):
        return None
    
    def history(self, param):
        return None

    def __init__(self, ui, app_id, ak, sk):
        self._conn = Conn(ui, app_id, ak, sk)
