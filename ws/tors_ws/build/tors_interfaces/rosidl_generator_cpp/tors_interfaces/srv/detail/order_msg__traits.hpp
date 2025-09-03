// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from tors_interfaces:srv/OrderMsg.idl
// generated code does not contain a copyright notice

#ifndef TORS_INTERFACES__SRV__DETAIL__ORDER_MSG__TRAITS_HPP_
#define TORS_INTERFACES__SRV__DETAIL__ORDER_MSG__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "tors_interfaces/srv/detail/order_msg__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace tors_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const OrderMsg_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: table_id
  {
    out << "table_id: ";
    rosidl_generator_traits::value_to_yaml(msg.table_id, out);
    out << ", ";
  }

  // member: client_order_id
  {
    out << "client_order_id: ";
    rosidl_generator_traits::value_to_yaml(msg.client_order_id, out);
    out << ", ";
  }

  // member: items_json
  {
    out << "items_json: ";
    rosidl_generator_traits::value_to_yaml(msg.items_json, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const OrderMsg_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: table_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "table_id: ";
    rosidl_generator_traits::value_to_yaml(msg.table_id, out);
    out << "\n";
  }

  // member: client_order_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "client_order_id: ";
    rosidl_generator_traits::value_to_yaml(msg.client_order_id, out);
    out << "\n";
  }

  // member: items_json
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "items_json: ";
    rosidl_generator_traits::value_to_yaml(msg.items_json, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const OrderMsg_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace tors_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use tors_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const tors_interfaces::srv::OrderMsg_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  tors_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use tors_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const tors_interfaces::srv::OrderMsg_Request & msg)
{
  return tors_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<tors_interfaces::srv::OrderMsg_Request>()
{
  return "tors_interfaces::srv::OrderMsg_Request";
}

template<>
inline const char * name<tors_interfaces::srv::OrderMsg_Request>()
{
  return "tors_interfaces/srv/OrderMsg_Request";
}

template<>
struct has_fixed_size<tors_interfaces::srv::OrderMsg_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<tors_interfaces::srv::OrderMsg_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<tors_interfaces::srv::OrderMsg_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace tors_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const OrderMsg_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: order_id
  {
    out << "order_id: ";
    rosidl_generator_traits::value_to_yaml(msg.order_id, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const OrderMsg_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: order_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "order_id: ";
    rosidl_generator_traits::value_to_yaml(msg.order_id, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const OrderMsg_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace tors_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use tors_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const tors_interfaces::srv::OrderMsg_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  tors_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use tors_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const tors_interfaces::srv::OrderMsg_Response & msg)
{
  return tors_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<tors_interfaces::srv::OrderMsg_Response>()
{
  return "tors_interfaces::srv::OrderMsg_Response";
}

template<>
inline const char * name<tors_interfaces::srv::OrderMsg_Response>()
{
  return "tors_interfaces/srv/OrderMsg_Response";
}

template<>
struct has_fixed_size<tors_interfaces::srv::OrderMsg_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<tors_interfaces::srv::OrderMsg_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<tors_interfaces::srv::OrderMsg_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<tors_interfaces::srv::OrderMsg>()
{
  return "tors_interfaces::srv::OrderMsg";
}

template<>
inline const char * name<tors_interfaces::srv::OrderMsg>()
{
  return "tors_interfaces/srv/OrderMsg";
}

template<>
struct has_fixed_size<tors_interfaces::srv::OrderMsg>
  : std::integral_constant<
    bool,
    has_fixed_size<tors_interfaces::srv::OrderMsg_Request>::value &&
    has_fixed_size<tors_interfaces::srv::OrderMsg_Response>::value
  >
{
};

template<>
struct has_bounded_size<tors_interfaces::srv::OrderMsg>
  : std::integral_constant<
    bool,
    has_bounded_size<tors_interfaces::srv::OrderMsg_Request>::value &&
    has_bounded_size<tors_interfaces::srv::OrderMsg_Response>::value
  >
{
};

template<>
struct is_service<tors_interfaces::srv::OrderMsg>
  : std::true_type
{
};

template<>
struct is_service_request<tors_interfaces::srv::OrderMsg_Request>
  : std::true_type
{
};

template<>
struct is_service_response<tors_interfaces::srv::OrderMsg_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // TORS_INTERFACES__SRV__DETAIL__ORDER_MSG__TRAITS_HPP_
