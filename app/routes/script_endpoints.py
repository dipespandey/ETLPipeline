"""
Myriad API 1.0
script_endpoints.py
..................
contains endpoints for script works using the API
"""
import os
import sys
import uuid
import json
import base64
import collections
from collections import OrderedDict
from flask import Response
from flask import Flask, make_response, render_template, Response, redirect
from flask import request, jsonify
import requests
from . import routes
from .myriad_logic import generate_muid
from models.rds import RDSWorks
from models.dynamo import Dynamo
from config import muid_creds, ref_creds
from models.myriad_custom_client_scripts import the_rake_script


@routes.route("/script-endpoints")
def test():
    return "This is myriadx api backend !"


@routes.route("/load-pixel", methods=['GET'])
def load_pixel():
    pixel_data = base64.b64decode(
        "R0lGODlhAQABAIAAAP8AAP8AACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==")
    thisdict = dict(request.args)
    print("Details in load-pixel end = ", thisdict)
    print("Pixel data = ", pixel_data)

    if "myriadx_muid" in thisdict:
        print("3rd party cookie is present in the cookie header")
        myriadx_muid = thisdict['myriadx_muid']
    else:
        # Generating the muid
        myriadx_muid = generate_muid()
        print("This is the new cookie_name", myriadx_muid)

    resp = Response(pixel_data, mimetype="image/gif")
    resp.set_cookie("myriadx_muid", myriadx_muid, secure=False,
                    expires=1551528000, path='/',  domain=".2pdx.co", httponly=True)

    return resp


@routes.route("/muid", methods=['GET', 'OPTIONS'])
def validate_muid():
    # checking if the cookie exists
    if "myriadx_muid" in request.cookies:
        print("3rd party cookie is present in the cookie header")
        myriadx_muid = request.cookies.get("myriadx_muid")
    else:
        # Generating the muid
        myriadx_muid = generate_muid()
        print("This is the new cookie_name", myriadx_muid)
    # setting the cookie
    resp = Response(myriadx_muid)
    # this will be used for stitch where our first party cookie is not there.
    return resp


@routes.route("/settings", methods=['GET'])
def loadSettings():
    cuid = request.args['cuid'].encode('ascii', 'ignore').decode()
    url = request.args['url'].encode('ascii', 'ignore').decode()
    # myriad website settings.
    print(type(cuid))
    settings = {}
    if cuid == "a64NNs59": # MYRIAD WEBSITE
        settings = {
            "cuid": cuid,
            "settings": "",
            "scripts": [

            ],
            "elements_to_track": [
                {
                    "element_id_type": "tag_name",
                    "element_id_value": "input",
                    "event_to_capture_on": "change"
                }
            ],
            "click_capture_exception_urls": [],
            "opt_out_status": False
        }
    elif cuid == "7CT37AtG": # PERGI settings
        settings = {
            "cuid": cuid,
            "settings": "",
            "scripts": [
                {
                    "pages_to_load_in": [
                        {
                            "match_type": "",
                            "url": ""
                        }
                    ],
                    "loading_pages": "",
                    "script_type": "",
                    "script": ""
                }
            ],
            "elements_to_track": [],
            "click_capture_exception_urls":  [
                {
                    "match_type": "regx",
                    "url": "pergi.com"
                }
            ],
            "opt_out_status": False
        }
    elif cuid == "4zm4shvX": # The RAKE settings
        settings = {
            "cuid": cuid,
            "settings": "",
            "scripts": [
                {
                    "pages_to_load_in": [
                        {
                            "match_type": "regx",
                            "url": "therake.com"
                        }
                    ],
                    "loading_pages": "",
                    "script_type": "",
                    "script": the_rake_script
                }
            ],
            "elements_to_track":  [
                {
                    "element_id_type": "name",
                    "element_id_value": "email",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "username",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "firstname",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "lastname",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "city",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "postcode",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "country_id",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "company",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "region",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "fax",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "coupon",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "shipping[firstname]",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "shipping[lastname]",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "shipping[city]",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "shipping[postcode]",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "shipping[country_id]",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "shipping[company]",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "shipping[region]",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "payment_method",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "FNAME",
                    "event_to_capture_on": "change"
                },
                {
                    "element_id_type": "name",
                    "element_id_value": "LNAME",
                    "event_to_capture_on": "change"
                }
            ],
            "click_capture_exception_urls": [],
            "opt_out_status": False
        }

    return json.dumps(settings, sort_keys=True)


@routes.route("/log", methods=['POST'])
def saveLogs():
    myriadx_log = request.get_json()
    print("myriad_log", myriadx_log)
    if myriadx_log is not None:
        ip_address = request.remote_addr or ''
        myriadx_log['ip_address'] = ip_address
        myriadx_muid = myriadx_log['muid']
        dyn = Dynamo()
        dyn.get_dynamodb_resource()
        dyn.insert_record(table='myriad-pixel-log-staging', record=myriadx_log)
        resp = make_response(jsonify({'myriadx_log': myriadx_log}))
        return resp


# vendor to myriad data sync
@routes.route("/vtm-data-sync", methods=['GET'])
def syncDataFromVendorToMyriad():
    # capture the vendor id, vendor uuid, redirect url, any other payload data
    vendor_id = request.args['vendor_id'].encode('ascii', 'ignore').decode()
    vendor_uuid = request.args['vendor_uuid'].encode(
        'ascii', 'ignore').decode()
    payload_data = request.args['payload_data'].encode(
        'ascii', 'ignore').decode()
    print(vendor_id, vendor_uuid, payload_data)
    if vendor_uuid is not None or len(vendor_uuid) > 0:
        # generate a new muid for the request if vendor uuid is not present in the vendor_uuid_muid_mappings table
        rds = RDSWorks(**muid_creds)
        rds.connect_to_db()
        if rds.get_muid_from_table(table='vendor_uuid_muid_mappings', value=('vendor_uuid', vendor_uuid), get='vendor_uuid') is None:
            muid = generate_muid()
            # log the vendor uuid against muid mapping to the vendor_uuid_muid_mappings table
            rds.insert_sql(table="vendor_uuid_muid_mappings", attrs=[
                "vendor_id", "vendor_uuid", "muid", "payload_data"], values=[
                1, vendor_uuid, muid, payload_data])
        rds.close_connection()
    return "This is vendor to myriad sync"


# myriad to vendor data sync
@routes.route("/mtv-data-sync", methods=['POST'])
def syncDataFromMyriadToVendor():
    # capture the muid from the request
    request_items = request.get_json()
    muid = request_items['muid']

    # TODO:
    # Do the db works in a queue
    # Return to the frontend first

    vendor_id = ""
    rds_ref = RDSWorks(**ref_creds)
    rds_muid = RDSWorks(**muid_creds)
    # get all the vendor records that has syncing enabled.
    rds_ref.connect_to_db()
    rds_muid.connect_to_db()
    get_query = "SELECT * from vendors where syncing_enabled=1"
    # vendors = ('id', 'vendor', 'vendor_id_for_myriad', 'partner_sync_url', 'sycing_enabled', 'status', 'created_at', 'updated_at')
    rds_ref.cursor.execute(get_query)
    results = rds_ref.cursor.fetchall()
    # for each vendor id check in the vendor_uuid_muid_mappings to see if there is a entry for a particular muid
    for result in results:
            # vendor_uuid_muid_mappings = ('id', 'vendor_id', 'vendor_uuid', 'muid', 'payload_data', 'created_at', 'updated_at')
        if rds_muid.get_muid_from_table(table='vendor_uuid_muid_mappings', value=('muid', muid), get='vendor_uuid') is None:
            # # if not send a request to vendor end point with muid

            # # get vendor end point for each vendor and vendor id
            vendor_end_point = "dpm.demdex.net/ibs:dpid=15&dpuuid=[MUID]&redir=[REDIRECT_URL]"

            # # prepare the redirect url as below
            redirect_url = "https://api.2pdx.co/vtm-data-sync?vendor_id=" + \
                vendor_id + "&muid="+muid+"&vuid=[REPLACE_WITH_YOUR_UUID]"

            # # append redirect url to vendor end point and send a post request
            vendor_end_point = vendor_end_point.replace('[MUID]', muid)
            vendor_end_point = vendor_end_point.replace('[REDIRECT_URL]', redirect_url)
            print(vendor_end_point)
            # redirect to vendor endpoint
            requests.get(vendor_end_point)
    rds_ref.close_connection()
    rds_muid.close_connection()

    return "Vendor sync done"


@routes.route("/log-values", methods=['POST'])
def logValues():
    # get the parameters from request
    request_dict = request.get_json()
    muid = request_dict.get("muid", "")
    cuid = request_dict.get("cuid", "")
    data_type = request_dict.get("data_type", "")
    hash_status = request_dict.get("hash_status", "")
    hash_method = request_dict.get("hash_method", "")
    applied_salt = request_dict.get("applied_salt", "")
    salt_position = request_dict.get("salt_position", "")
    attribute_type = request_dict.get("attribute_type", "")
    value = request_dict.get("value", "")

    if len(muid) > 0 and len(value) > 0:
        rds = RDSWorks(**muid_creds)
        rds.connect_to_db()
        # create a new record on either data or identity attribute table based on the data type that is being sent.
        if data_type == 'data_attributes':
            # send to data_attributes table
            if rds.get_muid_from_table(table='data_attributes', value=('value', value), get='muid') is None:
                rds.insert_sql(table='data_attributes', attrs=[
                               'muid', 'client_id', 'hash_status', 'hash_method', 'applied_salt', 'salt_position', 'attribute_type', 'value'],
                               values=[muid, cuid, hash_status, hash_method, applied_salt, salt_position, attribute_type, value])

        if data_type == 'identity_attributes':
            # send to identity_attributes table
            if rds.get_muid_from_table(table='identity_attributes', value=('value', value), get='muid') is None:
                rds.insert_sql(table='identity_attributes', attrs=[
                               'muid', 'client_id', 'hash_status', 'hash_method', 'applied_salt', 'salt_position', 'attribute_type', 'value'],
                               values=[muid, cuid, hash_status, hash_method, applied_salt, salt_position, attribute_type, value])
        rds.close_connection()
    return "Value updated successfully in production !"
