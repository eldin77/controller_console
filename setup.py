#!/usr/bin/env python
# -*- coding: utf8 -*-
from distutils.core import setup
setup(name="controller_console",
      version = "0.1",
      description = "SDN Controller Console App",
      author = "kobe",
      author_email = "katarina182818@gmail.com",
      data_files=[('conf',['conf/82ab2b55-96da-43c3-9c12-d785df9c5406.json',
                            'conf/controller_alias.json',
                            'conf/registered_controller.json',
                            'conf/test.json']),
                   ('tmp_conf',['tmp_conf/c4c86683-387a-4014-972a-2bbf1c8bbe31.json']),
                   ('document',['document/ONOS Installation guide.rtf',
                                'document/ONOS Rest API analysis.docx',
                                'document/README',
                                'document/odl_document/Excute_ODL_Error_v1.0.docx',
                                'document/odl_document/ODL_install_v1.0.docx',
                                'document/odl_document/Rest_Error_v1.0.docx',
                                'document/odl_document/odl_aaa_v1.0.docx',
                                'document/odl_document/Flow_API_v1.0.docx ',
                                'document/odl_document/ODL_restAPI_enable_v1.0.docx',
                                'document/odl_document/Switch_API_v1.0.docx'
                                ])
                            ],
      py_modules=["hp_api/config_hp_cmd","hp_api/config_hp_flows_cmd",
                    "hp_api/config_hp_switch_cmd", "controller_console",
                    "global_value", "hp_api/hp_controller_api",
                    "hp_api/hp_result_print","registered_controller","__init__",
                    "hp_api/__init__","utils"])

