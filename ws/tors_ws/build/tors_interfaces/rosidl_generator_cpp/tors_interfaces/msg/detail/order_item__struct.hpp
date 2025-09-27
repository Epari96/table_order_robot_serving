// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from tors_interfaces:msg/OrderItem.idl
// generated code does not contain a copyright notice

#ifndef TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__STRUCT_HPP_
#define TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__tors_interfaces__msg__OrderItem __attribute__((deprecated))
#else
# define DEPRECATED__tors_interfaces__msg__OrderItem __declspec(deprecated)
#endif

namespace tors_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct OrderItem_
{
  using Type = OrderItem_<ContainerAllocator>;

  explicit OrderItem_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->name = "";
      this->quantity = 0l;
    }
  }

  explicit OrderItem_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->name = "";
      this->quantity = 0l;
    }
  }

  // field types and members
  using _name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _name_type name;
  using _quantity_type =
    int32_t;
  _quantity_type quantity;

  // setters for named parameter idiom
  Type & set__name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->name = _arg;
    return *this;
  }
  Type & set__quantity(
    const int32_t & _arg)
  {
    this->quantity = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    tors_interfaces::msg::OrderItem_<ContainerAllocator> *;
  using ConstRawPtr =
    const tors_interfaces::msg::OrderItem_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<tors_interfaces::msg::OrderItem_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<tors_interfaces::msg::OrderItem_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      tors_interfaces::msg::OrderItem_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<tors_interfaces::msg::OrderItem_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      tors_interfaces::msg::OrderItem_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<tors_interfaces::msg::OrderItem_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<tors_interfaces::msg::OrderItem_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<tors_interfaces::msg::OrderItem_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__tors_interfaces__msg__OrderItem
    std::shared_ptr<tors_interfaces::msg::OrderItem_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__tors_interfaces__msg__OrderItem
    std::shared_ptr<tors_interfaces::msg::OrderItem_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const OrderItem_ & other) const
  {
    if (this->name != other.name) {
      return false;
    }
    if (this->quantity != other.quantity) {
      return false;
    }
    return true;
  }
  bool operator!=(const OrderItem_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct OrderItem_

// alias to use template instance with default allocator
using OrderItem =
  tors_interfaces::msg::OrderItem_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace tors_interfaces

#endif  // TORS_INTERFACES__MSG__DETAIL__ORDER_ITEM__STRUCT_HPP_
