// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from tors_interfaces:msg/OrderItem.idl
// generated code does not contain a copyright notice

#ifndef TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "tors_interfaces/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "tors_interfaces/msg/detail/order_item__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace tors_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_tors_interfaces
cdr_serialize(
  const tors_interfaces::msg::OrderItem & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_tors_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  tors_interfaces::msg::OrderItem & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_tors_interfaces
get_serialized_size(
  const tors_interfaces::msg::OrderItem & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_tors_interfaces
max_serialized_size_OrderItem(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace tors_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_tors_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, tors_interfaces, msg, OrderItem)();

#ifdef __cplusplus
}
#endif

#endif  // TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
