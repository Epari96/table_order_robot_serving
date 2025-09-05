// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from tors_interfaces:srv/OrderMsg.idl
// generated code does not contain a copyright notice

#ifndef TORS_INTERFACES__SRV__DETAIL__ORDER_MSG__BUILDER_HPP_
#define TORS_INTERFACES__SRV__DETAIL__ORDER_MSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "tors_interfaces/srv/detail/order_msg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace tors_interfaces
{

namespace srv
{

namespace builder
{

class Init_OrderMsg_Request_items
{
public:
  explicit Init_OrderMsg_Request_items(::tors_interfaces::srv::OrderMsg_Request & msg)
  : msg_(msg)
  {}
  ::tors_interfaces::srv::OrderMsg_Request items(::tors_interfaces::srv::OrderMsg_Request::_items_type arg)
  {
    msg_.items = std::move(arg);
    return std::move(msg_);
  }

private:
  ::tors_interfaces::srv::OrderMsg_Request msg_;
};

class Init_OrderMsg_Request_client_order_id
{
public:
  explicit Init_OrderMsg_Request_client_order_id(::tors_interfaces::srv::OrderMsg_Request & msg)
  : msg_(msg)
  {}
  Init_OrderMsg_Request_items client_order_id(::tors_interfaces::srv::OrderMsg_Request::_client_order_id_type arg)
  {
    msg_.client_order_id = std::move(arg);
    return Init_OrderMsg_Request_items(msg_);
  }

private:
  ::tors_interfaces::srv::OrderMsg_Request msg_;
};

class Init_OrderMsg_Request_table_id
{
public:
  Init_OrderMsg_Request_table_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_OrderMsg_Request_client_order_id table_id(::tors_interfaces::srv::OrderMsg_Request::_table_id_type arg)
  {
    msg_.table_id = std::move(arg);
    return Init_OrderMsg_Request_client_order_id(msg_);
  }

private:
  ::tors_interfaces::srv::OrderMsg_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::tors_interfaces::srv::OrderMsg_Request>()
{
  return tors_interfaces::srv::builder::Init_OrderMsg_Request_table_id();
}

}  // namespace tors_interfaces


namespace tors_interfaces
{

namespace srv
{

namespace builder
{

class Init_OrderMsg_Response_message
{
public:
  explicit Init_OrderMsg_Response_message(::tors_interfaces::srv::OrderMsg_Response & msg)
  : msg_(msg)
  {}
  ::tors_interfaces::srv::OrderMsg_Response message(::tors_interfaces::srv::OrderMsg_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::tors_interfaces::srv::OrderMsg_Response msg_;
};

class Init_OrderMsg_Response_accepted
{
public:
  Init_OrderMsg_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_OrderMsg_Response_message accepted(::tors_interfaces::srv::OrderMsg_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_OrderMsg_Response_message(msg_);
  }

private:
  ::tors_interfaces::srv::OrderMsg_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::tors_interfaces::srv::OrderMsg_Response>()
{
  return tors_interfaces::srv::builder::Init_OrderMsg_Response_accepted();
}

}  // namespace tors_interfaces

#endif  // TORS_INTERFACES__SRV__DETAIL__ORDER_MSG__BUILDER_HPP_
