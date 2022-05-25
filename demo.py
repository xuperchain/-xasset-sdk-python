#!/usr/bin python3
# -*- coding: utf-8 -*-
# @file       : demo.py
# @create time: 2022/05/25
# @说明       : 本文件提供了调起ui的测试用例
#               本测试环境为python3.7.3
#               可通过执行 python setup.py install 安装xassetsdk包
#               也可通过自行打包，推荐使用虚拟环境后获取依赖包版本，使用setuptools打包，注意setup.py依赖
#               install xassetsdk 成功后，执行本文件即可

from xasset.client.client import Client
from xasset.auth.account import XassetAccount

import time
from xasset.utils.utils import Utils

'''
配置
'''
UI = ""
AppID = 0
AK = ""
SK = ""

'''
资产和碎片状态
'''
AssetStatusPublished = 4
ShardStatusOnChain = 0
ShardsStatusConsumed = 6

def test():
    xasset = Client(UI, AppID, AK, SK)
    account_a_json = {
        'addr': 'TeyyPLpp9L7QAcxHangtcHTu7HUZ6iydY',
        'sk': '{"Curvname":"P-256","X":36505150171354363400464126431978257855318414556425194490762274938603757905292,"Y":79656876957602994269528255245092635964473154458596947290316223079846501380076,"D":111497060296999106528800133634901141644446751975433315540300236500052690483486}',
    }
    account_a = XassetAccount(account_a_json['addr'], account_a_json['sk'])
    account_b_json = {
        'addr': 'SmJG3rH2ZzYQ9ojxhbRCPwFiE9y6pD1Co',
        'sk': '{"Curvname":"P-256","X":12866043091588565003171939933628544430893620588191336136713947797738961176765,"Y":82755103183873558994270855453149717093321792154549800459286614469868720031056,"D":74053182141043989390619716280199465858509830752513286817516873984288039572219}',
    }      

    # get stoken
    print("------- test get stoken -------")
    stoken_param = {
        'account': {
            'addr': account_a_json['addr'],
            'sk': account_a_json['sk'],
        },
    }
    stoken_result = xasset.get_stoken(stoken_param)
    if stoken_result is None:
        return None


    # create asset
    print("------- test create asset -------")
    create_param = {
        'price': 10010,
        'amount': 100,
        'asset_info': {
            'asset_cate': 1,
            'title': '我是一个小画家',
            'thumb': ["bos_v1://bucket/object/1000_500"],
            'short_desc': '我是一个小画家',
            'img_desc': ["bos_v1://bucket/object/1000_500"],
            'asset_url': ["bos_v1://bucket/object/1000_500"],
        },
        'account': {
            'addr': account_a_json['addr'],
            'sk': account_a_json['sk'],
        },
    }
    asset_id = xasset.create_asset(create_param)
    if asset_id is None:
        return None
    

    # alter asset
    print("------- test alter asset -------")
    alter_param = {
        'asset_id': asset_id,
        'account': {
            'addr': account_a_json['addr'],
            'sk': account_a_json['sk'],
        },
        'amount': -1, # 'amount'和'price'如果没有修改需求，需要置为-1，其余参数零值即可
        'price': 20010,
    }
    alter_result = xasset.alter_asset(alter_param)
    if alter_result is None:
        return None


    # publish asset
    publish_param = {
        'asset_id': asset_id,
        'account': {
            'addr': account_a_json['addr'],
            'sk': account_a_json['sk'],
        },
    }
    print("------- test publish asset -------")
    errno = xasset.publish_asset(publish_param)
    if errno is None:
        return None


    # query asset
    print("------- check asset published -------")
    meta = xasset.query_asset(asset_id)

    if meta is None:
        return None
    while meta['status'] != AssetStatusPublished:
        time.sleep(30)
        meta = xasset.query_asset(asset_id)


    # grant shard
    print("------- test grant asset -------")
    grant_param = {
        'asset_id': asset_id,
        'price': 20020,
        'shard_id': Utils.gen_nonce(),
        'to_addr': 'SmJG3rH2ZzYQ9ojxhbRCPwFiE9y6pD1Co',
        'account': {
            'addr': account_a_json['addr'],
            'sk': account_a_json['sk'],
        },
    }
    resp = xasset.grant_shard(grant_param)
    if resp is None:
        return None
    shard_id = resp['shard_id']


    # query shard
    print("------- check shard on chain -------")
    querysrd_param = {
        'asset_id': asset_id,
        'shard_id': shard_id,
    }
    shard_info = xasset.query_shard(querysrd_param)
    if shard_info is None:
        return None
    while shard_info['status'] != ShardStatusOnChain:
        time.sleep(30)
        shard_info = xasset.query_shard(querysrd_param)
    

    # transfer shard
    print("------- test transfer shard -------")
    transfer_param = {
        'asset_id': asset_id,
        'shard_id': shard_id,
        'to_addr': account_a_json['addr'],
        'account': {
            'addr': account_b_json['addr'],
            'sk': account_b_json['sk'], 
        },
    }
    resp = xasset.transfer_shard(transfer_param)
    if resp is None:
        return None
    

    # query shard
    print("------- check shard on chain -------")
    querysrd_param = {
        'asset_id': asset_id,
        'shard_id': shard_id,
    }
    shard_info = xasset.query_shard(querysrd_param)
    if shard_info is None:
        return None
    while shard_info['status'] != ShardStatusOnChain:
        time.sleep(30)
        shard_info = xasset.query_shard(querysrd_param)
    

    # consume shard
    print("------- test consume shard -------")
    nonce = Utils.gen_nonce()
    creator_signMsg = '%d%d' % (asset_id, nonce)
    creator_sign = account_a.sign_ecdsa(creator_signMsg)
    consume_param = {
        'asset_id': asset_id,
        'shard_id': shard_id,
        'create_account': {
            'addr': account_a_json['addr'],
            'sk': account_a_json['sk'],
        },
        'user_addr': account_a_json['addr'],
        'nonce': nonce,
        'user_sign': creator_sign,
        'user_pkey': account_a.public_key(),
    }
    resp = xasset.consume_shard(consume_param)
    if resp is None:
        return None
    

    # query shard
    print("------- check shard consumed -------")
    querysrd_param = {
        'asset_id': asset_id,
        'shard_id': shard_id,
    }
    shard_info = xasset.query_shard(querysrd_param)
    if shard_info is None:
        return None
    while shard_info['status'] != ShardsStatusConsumed:
        time.sleep(30)
        shard_info = xasset.query_shard(querysrd_param)
    

    # freeze asset
    print("------- test freeze asset -------")
    freeze_param = {
        'asset_id': asset_id,
        'account': {
            'addr': account_a_json['addr'],
            'sk': account_a_json['sk'],
        },
    }
    print(xasset.freeze_asset(freeze_param))


    # list asset by address
    print("------- test list_asset_by_addr -------")
    list_a = xasset.list_asset_by_addr(0, "SmJG3rH2ZzYQ9ojxhbRCPwFiE9y6pD1Co", 1)
    if list_a is None:
        return None
    print(list_a)


    # list shards by address
    print("------- test list_shards_by_addr -------")
    list_b = xasset.list_shards_by_addr("SmJG3rH2ZzYQ9ojxhbRCPwFiE9y6pD1Co", 1)
    if list_b is None:
        return None
    print(list_b)


    # list shards by asset
    print("------- test list_shards_by_asset -------")
    list_c = xasset.list_shards_by_asset(asset_id, "", 20)
    if list_c is None:
        return None
    print(list_c)


    # list history
    print("------- test list history -------")
    list_d = xasset.history(asset_id, 1)
    if list_d is None:
        return None
    print(list_d)


if __name__ == '__main__':
    test()