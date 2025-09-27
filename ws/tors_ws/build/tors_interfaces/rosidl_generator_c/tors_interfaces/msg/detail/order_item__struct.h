// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from tors_interfaces:msg/OrderItem.idl
// generated code does not contain a copyright notice

#ifndef TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__STRUCT_H_
#define TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/OrderItem in the package tors_interfaces.
typedef struct tors_interfaces__msg__OrderItem
{
  rosidl_runtime_c__String name;
  int32_t quantity;
} tors_interfaces__msg__OrderItem;

// Struct for a sequence of tors_interfaces__msg__OrderItem.
typedef struct tors_interfaces__msg__OrderItem__Sequence
{
  tors_interfaces__msg__OrderItem * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} tors_interfaces__msg__OrderItem__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__STRUCT_H_
