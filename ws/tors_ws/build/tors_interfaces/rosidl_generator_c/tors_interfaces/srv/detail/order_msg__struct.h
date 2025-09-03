// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from tors_interfaces:srv/OrderMsg.idl
// generated code does not contain a copyright notice

#ifndef TORS_INTERFACES__SRV__DETAIL__ORDER_MSG__STRUCT_H_
#define TORS_INTERFACES__SRV__DETAIL__ORDER_MSG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'table_id'
// Member 'client_order_id'
// Member 'items_json'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/OrderMsg in the package tors_interfaces.
typedef struct tors_interfaces__srv__OrderMsg_Request
{
  /// "T12"
  rosidl_runtime_c__String table_id;
  /// UUID from GUI (idempotency key)
  rosidl_runtime_c__String client_order_id;
  /// {"비빔밥":2,"물":1,"옵션":{"맵기":"보통"}}
  rosidl_runtime_c__String items_json;
} tors_interfaces__srv__OrderMsg_Request;

// Struct for a sequence of tors_interfaces__srv__OrderMsg_Request.
typedef struct tors_interfaces__srv__OrderMsg_Request__Sequence
{
  tors_interfaces__srv__OrderMsg_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} tors_interfaces__srv__OrderMsg_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'order_id'
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/OrderMsg in the package tors_interfaces.
typedef struct tors_interfaces__srv__OrderMsg_Response
{
  /// 수락/거절
  bool accepted;
  /// 서버 발급 고유 ID (DB PK)
  rosidl_runtime_c__String order_id;
  /// 안내/사유(품절 등)
  rosidl_runtime_c__String message;
} tors_interfaces__srv__OrderMsg_Response;

// Struct for a sequence of tors_interfaces__srv__OrderMsg_Response.
typedef struct tors_interfaces__srv__OrderMsg_Response__Sequence
{
  tors_interfaces__srv__OrderMsg_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} tors_interfaces__srv__OrderMsg_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TORS_INTERFACES__SRV__DETAIL__ORDER_MSG__STRUCT_H_
