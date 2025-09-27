// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from tors_interfaces:msg/OrderItem.idl
// generated code does not contain a copyright notice
#include "tors_interfaces/msg/detail/order_item__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `name`
#include "rosidl_runtime_c/string_functions.h"

bool
tors_interfaces__msg__OrderItem__init(tors_interfaces__msg__OrderItem * msg)
{
  if (!msg) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__init(&msg->name)) {
    tors_interfaces__msg__OrderItem__fini(msg);
    return false;
  }
  // quantity
  return true;
}

void
tors_interfaces__msg__OrderItem__fini(tors_interfaces__msg__OrderItem * msg)
{
  if (!msg) {
    return;
  }
  // name
  rosidl_runtime_c__String__fini(&msg->name);
  // quantity
}

bool
tors_interfaces__msg__OrderItem__are_equal(const tors_interfaces__msg__OrderItem * lhs, const tors_interfaces__msg__OrderItem * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->name), &(rhs->name)))
  {
    return false;
  }
  // quantity
  if (lhs->quantity != rhs->quantity) {
    return false;
  }
  return true;
}

bool
tors_interfaces__msg__OrderItem__copy(
  const tors_interfaces__msg__OrderItem * input,
  tors_interfaces__msg__OrderItem * output)
{
  if (!input || !output) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__copy(
      &(input->name), &(output->name)))
  {
    return false;
  }
  // quantity
  output->quantity = input->quantity;
  return true;
}

tors_interfaces__msg__OrderItem *
tors_interfaces__msg__OrderItem__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tors_interfaces__msg__OrderItem * msg = (tors_interfaces__msg__OrderItem *)allocator.allocate(sizeof(tors_interfaces__msg__OrderItem), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(tors_interfaces__msg__OrderItem));
  bool success = tors_interfaces__msg__OrderItem__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
tors_interfaces__msg__OrderItem__destroy(tors_interfaces__msg__OrderItem * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    tors_interfaces__msg__OrderItem__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
tors_interfaces__msg__OrderItem__Sequence__init(tors_interfaces__msg__OrderItem__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tors_interfaces__msg__OrderItem * data = NULL;

  if (size) {
    data = (tors_interfaces__msg__OrderItem *)allocator.zero_allocate(size, sizeof(tors_interfaces__msg__OrderItem), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = tors_interfaces__msg__OrderItem__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        tors_interfaces__msg__OrderItem__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
tors_interfaces__msg__OrderItem__Sequence__fini(tors_interfaces__msg__OrderItem__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      tors_interfaces__msg__OrderItem__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

tors_interfaces__msg__OrderItem__Sequence *
tors_interfaces__msg__OrderItem__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tors_interfaces__msg__OrderItem__Sequence * array = (tors_interfaces__msg__OrderItem__Sequence *)allocator.allocate(sizeof(tors_interfaces__msg__OrderItem__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = tors_interfaces__msg__OrderItem__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
tors_interfaces__msg__OrderItem__Sequence__destroy(tors_interfaces__msg__OrderItem__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    tors_interfaces__msg__OrderItem__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
tors_interfaces__msg__OrderItem__Sequence__are_equal(const tors_interfaces__msg__OrderItem__Sequence * lhs, const tors_interfaces__msg__OrderItem__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!tors_interfaces__msg__OrderItem__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
tors_interfaces__msg__OrderItem__Sequence__copy(
  const tors_interfaces__msg__OrderItem__Sequence * input,
  tors_interfaces__msg__OrderItem__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(tors_interfaces__msg__OrderItem);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    tors_interfaces__msg__OrderItem * data =
      (tors_interfaces__msg__OrderItem *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!tors_interfaces__msg__OrderItem__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          tors_interfaces__msg__OrderItem__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!tors_interfaces__msg__OrderItem__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
