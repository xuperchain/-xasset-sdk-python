#!/usr/bin python3
# -*- coding: utf-8 -*-
# @file       : conn.py
# @create time: 2022/05/24
# @说明       : 本文件实现了各api参数的鉴权逻辑

from threading import stack_size
from numpy import int64
from xasset.utils.utils import Utils
from xasset.auth.account import XassetAccount

class Param(object):
    @staticmethod
    def sign_msg(asset_id, account_json):
        nonce = Utils.gen_nonce()
        addr = account_json['addr']
        sk = account_json['sk']
        account = XassetAccount(addr, sk)
        signMsg = '%d%d' % (asset_id, nonce)
        sign = account.sign_ecdsa(signMsg)
        data = {
            'nonce': nonce,
            'addr': addr,
            'pkey': account.public_key(),
            'sign': sign,
        }
        return data

    @staticmethod
    def query_shard_valid(param):
        if 'asset_id' not in param:
            return False
        if 'shard_id' not in param:
            return False
        if param['asset_id'] < 0 or param['shard_id'] < 0:
            return False
        return True

    @staticmethod
    def account_valid(param):
        if 'addr' not in param:
            return False
        if param['addr'] == '':
            return False
        if 'sk' not in param:
            return False
        if param['sk'] == '':
            return False
        return True

    @staticmethod
    def create_asset_valid(param):
        if 'amount' not in param:
            return False
        if 'price' not in param:
            return False

        if 'account' not in param:
            return False
        if not Param.account_valid(param['account']):
            return False

        if 'asset_info' not in param:
            return False
        if not Param.asset_info_valid(param['asset_info']):
            return False
        return True

    @staticmethod
    def asset_info_valid(param):
        if 'asset_cate' not in param:
            return False
        if 'title' not in param:
            return False

        if 'thumb' not in param:
            return False
        if not isinstance(param['thumb'], list):
            return False

        if 'short_desc' not in param:
            return False
        if 'asset_url' not in param:
            return False

        if not isinstance(param['asset_url'], list):
            return False

        if 'img_desc' in param.keys():
            if not isinstance(param['img_desc'], list):
                return False

        if 'long_desc' in param.keys():
            if not isinstance(param['long_desc'], str):
                return False

        if 'asset_ext' in param.keys():
            if not isinstance(param['asset_ext'], str):
                return False

        if 'group_id' in param.keys():
            if not isinstance(param['group_id'], int64):
                return False
        return True

    @staticmethod
    def alter_valid(param):
        if 'asset_id' not in param:
            return False
            
        price_check = False
        if 'amount' in param.keys():
            amount_check = True

        price_check = False
        if 'price' in param.keys():
            price_check = True

        info_check = False
        if 'asset_info' in param.keys():
            info_check = True
        return price_check or price_check or info_check
      
    @staticmethod
    def publish_valid(param):
        if 'asset_id' not in param:
            return False
        if 'evidence_type' in param.keys():
              if not isinstance(param['evidence_type'], int):
                return False
        return True

    @staticmethod
    def freeze_valid(param):
        if 'asset_id' not in param:
            return False
        if 'account' not in param:
            return False
        if not Param.account_valid(param['account']):
            return False
        return True

    @staticmethod
    def consume_valid(param):
        if 'asset_id' not in param:
            return False
        if 'nonce' not in param:
            return False
        if 'shard_id' not in param:
            return False

        if 'create_account' not in param:
            return False
        if not Param.account_valid(param['create_account']):
            return False
        
        if 'user_addr' not in param:
            return False
        if 'user_sign' not in param:
            return False
        if 'user_pkey' not in param:
            return False
        return True

    @staticmethod
    def grant_valid(param):
        if 'asset_id' not in param:
            return False
        if 'account' not in param:
            return False
        if not Param.account_valid(param['account']):
            return False
        if 'to_addr' not in param:
            return False
        return True

    @staticmethod
    def transfer_valid(param):
        if 'asset_id' not in param:
            return False
        if 'account' not in param:
            return False
        if 'shard_id' not in param:
            return False
        if 'to_addr' not in param:
            return False
        