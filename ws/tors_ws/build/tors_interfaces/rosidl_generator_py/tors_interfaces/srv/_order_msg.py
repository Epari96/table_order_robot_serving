# generated from rosidl_generator_py/resource/_idl.py.em
# with input from tors_interfaces:srv/OrderMsg.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_OrderMsg_Request(type):
    """Metaclass of message 'OrderMsg_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('tors_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'tors_interfaces.srv.OrderMsg_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__order_msg__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__order_msg__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__order_msg__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__order_msg__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__order_msg__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class OrderMsg_Request(metaclass=Metaclass_OrderMsg_Request):
    """Message class 'OrderMsg_Request'."""

    __slots__ = [
        '_table_id',
        '_client_order_id',
        '_items_json',
    ]

    _fields_and_field_types = {
        'table_id': 'string',
        'client_order_id': 'string',
        'items_json': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.table_id = kwargs.get('table_id', str())
        self.client_order_id = kwargs.get('client_order_id', str())
        self.items_json = kwargs.get('items_json', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.table_id != other.table_id:
            return False
        if self.client_order_id != other.client_order_id:
            return False
        if self.items_json != other.items_json:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def table_id(self):
        """Message field 'table_id'."""
        return self._table_id

    @table_id.setter
    def table_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'table_id' field must be of type 'str'"
        self._table_id = value

    @builtins.property
    def client_order_id(self):
        """Message field 'client_order_id'."""
        return self._client_order_id

    @client_order_id.setter
    def client_order_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'client_order_id' field must be of type 'str'"
        self._client_order_id = value

    @builtins.property
    def items_json(self):
        """Message field 'items_json'."""
        return self._items_json

    @items_json.setter
    def items_json(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'items_json' field must be of type 'str'"
        self._items_json = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_OrderMsg_Response(type):
    """Metaclass of message 'OrderMsg_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('tors_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'tors_interfaces.srv.OrderMsg_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__order_msg__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__order_msg__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__order_msg__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__order_msg__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__order_msg__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class OrderMsg_Response(metaclass=Metaclass_OrderMsg_Response):
    """Message class 'OrderMsg_Response'."""

    __slots__ = [
        '_accepted',
        '_order_id',
        '_message',
    ]

    _fields_and_field_types = {
        'accepted': 'boolean',
        'order_id': 'string',
        'message': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.accepted = kwargs.get('accepted', bool())
        self.order_id = kwargs.get('order_id', str())
        self.message = kwargs.get('message', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.accepted != other.accepted:
            return False
        if self.order_id != other.order_id:
            return False
        if self.message != other.message:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def accepted(self):
        """Message field 'accepted'."""
        return self._accepted

    @accepted.setter
    def accepted(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'accepted' field must be of type 'bool'"
        self._accepted = value

    @builtins.property
    def order_id(self):
        """Message field 'order_id'."""
        return self._order_id

    @order_id.setter
    def order_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'order_id' field must be of type 'str'"
        self._order_id = value

    @builtins.property
    def message(self):
        """Message field 'message'."""
        return self._message

    @message.setter
    def message(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'message' field must be of type 'str'"
        self._message = value


class Metaclass_OrderMsg(type):
    """Metaclass of service 'OrderMsg'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('tors_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'tors_interfaces.srv.OrderMsg')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__order_msg

            from tors_interfaces.srv import _order_msg
            if _order_msg.Metaclass_OrderMsg_Request._TYPE_SUPPORT is None:
                _order_msg.Metaclass_OrderMsg_Request.__import_type_support__()
            if _order_msg.Metaclass_OrderMsg_Response._TYPE_SUPPORT is None:
                _order_msg.Metaclass_OrderMsg_Response.__import_type_support__()


class OrderMsg(metaclass=Metaclass_OrderMsg):
    from tors_interfaces.srv._order_msg import OrderMsg_Request as Request
    from tors_interfaces.srv._order_msg import OrderMsg_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
