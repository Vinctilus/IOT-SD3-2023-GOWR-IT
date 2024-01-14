#Classe Code
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.models.consumer.v3.channel import Channel
from pubnub.models.consumer.v3.uuid import UUID
from .env import env

cipher_key = env["PIRVAT_PN_cipher_key"]



pn_config = PNConfiguration()
pn_config.publish_key = env["USER_PUBNUB_PUBLISH_KEY"]
pn_config.subscribe_key = env["USER_PUBNUB_SUBSCRIBE_KEY"]
pn_config.uuid = "SERVER"
pn_config.secret_key = env["USER_SECRET_KEY"]
pn_config.cipher_key = cipher_key
pubnub = PubNub(pn_config)


def grant_read_access(user_id):
    channels = [
            Channel.id(str(user_id)).read()
            ]
    uuids = [
            UUID.id("uuid-d").get().update()
            ]
    envelope = pubnub.grant_token().channels(channels).ttl(15).uuids(uuids).authorized_uuid(user_id).sync()
    return envelope.result.token


def grant_read_write_access(server,user_id):
    channels = [
            Channel.id(str(user_id)).read().write()
            ]
    uuids = [
            UUID.id("uuid-d").get().update()
            ]
    envelope = pubnub.grant_token().channels(channels).ttl(15).uuids(uuids).authorized_uuid(server).sync()
    return envelope.result.token


def revoke_acess(token):
    envelope = pubnub.revoke_token(token).sync()


def parse_token(token):
    token_details = pubnub.parse_token(token)
    print(token_details)
    read_access = token_details['resources']['channels']['johns_sd3a_pi']['read']
    write_access = token_details['resources']['channels']['johns_sd3a_pi']['write']
    uuid = token_details['authorized_uuid']
    return token_details['timestamp'], token_details['ttl'], uuid, read_access, write_access