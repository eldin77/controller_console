# CMD_tree
Controller#
     ├-add
     │  └-type(HP, ODL, ONOS), controller_IP, port
     │
     ├-show
     │  ├-controller_name
     │  └-all
     │
     ├-config
     │  └-controller_IP:
     │          └-config(controller_name)
     │               ├-show
     │               │   ├-switches
     │               │   ├-hosts
     │               │   ├-links
     │               │   ├-flows
     │               │   └-controller_info
     │               │
     │               ├-switch
     │               │   └-switch-name
     │               │       └-controller(switch-name)#
     │               │           ├-alias
     │               │           │   └-alias <new-name>
     │               │           │
     │               │           ├-show
     │               │           │   ├-ports
     │               │           │   └-flows
     │               │           │
     │               │           ├-make-flow
     │               │           │   └- open_flow_match_pattern
     │               │           │
     │               │           ├-help
     │               │           ├-quit
     │               │           └-exit
     │               │
     │               ├-alias(controller_unique_name)
     │               │
     │               ├-help
     │               └-exit
     │
     ├-help
     ├-exit
     └-quit
