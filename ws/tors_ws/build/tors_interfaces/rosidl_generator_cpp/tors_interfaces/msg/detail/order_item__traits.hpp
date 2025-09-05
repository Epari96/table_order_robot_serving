// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from tors_interfaces:msg/OrderItem.idl
// generated code does not contain a copyright notice

#ifndef TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__TRAITS_HPP_
#define TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "tors_interfaces/msg/detail/order_item__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace tors_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const OrderItem & msg,
  std::ostream & out)
{
  out << "{";
  // member: name
  {
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << ", ";
  }

  // member: quantity
  {
    out << "quantity: ";
    rosidl_generator_traits::value_to_yaml(msg.quantity, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const OrderItem & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << "\n";
  }

  // member: quantity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "quantity: ";
    rosidl_generator_traits::value_to_yaml(msg.quantity, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const OrderItem & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace tors_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use tors_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const tors_interfaces::msg::OrderItem & msg,
  std::ostream & out, size_t indentation = 0)
{
  tors_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use tors_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const tors_interfaces::msg::OrderItem & msg)
{
  return tors_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<tors_interfaces::msg::OrderItem>()
{
  return "tors_interfaces::msg::OrderItem";
}

template<>
inline const char * name<tors_interfaces::msg::OrderItem>()
{
  return "tors_interfaces/msg/OrderItem";
}

template<>
struct has_fixed_size<tors_interfaces::msg::OrderItem>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<tors_interfaces::msg::OrderItem>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<tors_interfaces::msg::OrderItem>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__TRAITS_HPP_
