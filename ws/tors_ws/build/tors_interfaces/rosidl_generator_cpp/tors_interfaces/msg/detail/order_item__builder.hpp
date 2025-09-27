// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from tors_interfaces:msg/OrderItem.idl
// generated code does not contain a copyright notice

#ifndef TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__BUILDER_HPP_
#define TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "tors_interfaces/msg/detail/order_item__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace tors_interfaces
{

namespace msg
{

namespace builder
{

class Init_OrderItem_quantity
{
public:
  explicit Init_OrderItem_quantity(::tors_interfaces::msg::OrderItem & msg)
  : msg_(msg)
  {}
  ::tors_interfaces::msg::OrderItem quantity(::tors_interfaces::msg::OrderItem::_quantity_type arg)
  {
    msg_.quantity = std::move(arg);
    return std::move(msg_);
  }

private:
  ::tors_interfaces::msg::OrderItem msg_;
};

class Init_OrderItem_name
{
public:
  Init_OrderItem_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_OrderItem_quantity name(::tors_interfaces::msg::OrderItem::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_OrderItem_quantity(msg_);
  }

private:
  ::tors_interfaces::msg::OrderItem msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::tors_interfaces::msg::OrderItem>()
{
  return tors_interfaces::msg::builder::Init_OrderItem_name();
}

}  // namespace tors_interfaces

#endif  // TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__BUILDER_HPP_
