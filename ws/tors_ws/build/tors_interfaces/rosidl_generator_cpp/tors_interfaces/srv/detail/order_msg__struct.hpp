// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from tors_interfaces:srv/OrderMsg.idl
// generated code does not contain a copyright notice

#ifndef TORS_INTERFACES__SRV__DETAIL__ORDER_MSG__STRUCT_HPP_
#define TORS_INTERFACES__SRV__DETAIL__ORDER_MSG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__tors_interfaces__srv__OrderMsg_Request __attribute__((deprecated))
#else
# define DEPRECATED__tors_interfaces__srv__OrderMsg_Request __declspec(deprecated)
#endif

namespace tors_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct OrderMsg_Request_
{
  using Type = OrderMsg_Request_<ContainerAllocator>;

  explicit OrderMsg_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->table_id = "";
      this->client_order_id = "";
      this->items_json = "";
    }
  }

  explicit OrderMsg_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : table_id(_alloc),
    client_order_id(_alloc),
    items_json(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->table_id = "";
      this->client_order_id = "";
      this->items_json = "";
    }
  }

  // field types and members
  using _table_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _table_id_type table_id;
  using _client_order_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _client_order_id_type client_order_id;
  using _items_json_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _items_json_type items_json;

  // setters for named parameter idiom
  Type & set__table_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->table_id = _arg;
    return *this;
  }
  Type & set__client_order_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->client_order_id = _arg;
    return *this;
  }
  Type & set__items_json(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->items_json = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    tors_interfaces::srv::OrderMsg_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const tors_interfaces::srv::OrderMsg_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<tors_interfaces::srv::OrderMsg_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<tors_interfaces::srv::OrderMsg_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      tors_interfaces::srv::OrderMsg_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<tors_interfaces::srv::OrderMsg_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      tors_interfaces::srv::OrderMsg_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<tors_interfaces::srv::OrderMsg_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<tors_interfaces::srv::OrderMsg_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<tors_interfaces::srv::OrderMsg_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__tors_interfaces__srv__OrderMsg_Request
    std::shared_ptr<tors_interfaces::srv::OrderMsg_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__tors_interfaces__srv__OrderMsg_Request
    std::shared_ptr<tors_interfaces::srv::OrderMsg_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const OrderMsg_Request_ & other) const
  {
    if (this->table_id != other.table_id) {
      return false;
    }
    if (this->client_order_id != other.client_order_id) {
      return false;
    }
    if (this->items_json != other.items_json) {
      return false;
    }
    return true;
  }
  bool operator!=(const OrderMsg_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct OrderMsg_Request_

// alias to use template instance with default allocator
using OrderMsg_Request =
  tors_interfaces::srv::OrderMsg_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace tors_interfaces


#ifndef _WIN32
# define DEPRECATED__tors_interfaces__srv__OrderMsg_Response __attribute__((deprecated))
#else
# define DEPRECATED__tors_interfaces__srv__OrderMsg_Response __declspec(deprecated)
#endif

namespace tors_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct OrderMsg_Response_
{
  using Type = OrderMsg_Response_<ContainerAllocator>;

  explicit OrderMsg_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
      this->order_id = "";
      this->message = "";
    }
  }

  explicit OrderMsg_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : order_id(_alloc),
    message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
      this->order_id = "";
      this->message = "";
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _order_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _order_id_type order_id;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__order_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->order_id = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    tors_interfaces::srv::OrderMsg_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const tors_interfaces::srv::OrderMsg_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<tors_interfaces::srv::OrderMsg_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<tors_interfaces::srv::OrderMsg_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      tors_interfaces::srv::OrderMsg_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<tors_interfaces::srv::OrderMsg_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      tors_interfaces::srv::OrderMsg_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<tors_interfaces::srv::OrderMsg_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<tors_interfaces::srv::OrderMsg_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<tors_interfaces::srv::OrderMsg_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__tors_interfaces__srv__OrderMsg_Response
    std::shared_ptr<tors_interfaces::srv::OrderMsg_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__tors_interfaces__srv__OrderMsg_Response
    std::shared_ptr<tors_interfaces::srv::OrderMsg_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const OrderMsg_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->order_id != other.order_id) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const OrderMsg_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct OrderMsg_Response_

// alias to use template instance with default allocator
using OrderMsg_Response =
  tors_interfaces::srv::OrderMsg_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace tors_interfaces

namespace tors_interfaces
{

namespace srv
{

struct OrderMsg
{
  using Request = tors_interfaces::srv::OrderMsg_Request;
  using Response = tors_interfaces::srv::OrderMsg_Response;
};

}  // namespace srv

}  // namespace tors_interfaces

#endif  // TORS_INTERFACES__SRV__DETAIL__ORDER_MSG__STRUCT_HPP_
