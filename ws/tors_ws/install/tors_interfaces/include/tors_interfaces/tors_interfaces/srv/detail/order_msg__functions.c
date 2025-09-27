// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from tors_interfaces:srv/OrderMsg.idl
// generated code does not contain a copyright notice
#include "tors_interfaces/srv/detail/order_msg__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `client_order_id`
// Member `items_json`
#include "rosidl_runtime_c/string_functions.h"

bool
tors_interfaces__srv__OrderMsg_Request__init(tors_interfaces__srv__OrderMsg_Request * msg)
{
  if (!msg) {
    return false;
  }
  // table_id
  // client_order_id
  if (!rosidl_runtime_c__String__init(&msg->client_order_id)) {
    tors_interfaces__srv__OrderMsg_Request__fini(msg);
    return false;
  }
  // items_json
  if (!rosidl_runtime_c__String__init(&msg->items_json)) {
    tors_interfaces__srv__OrderMsg_Request__fini(msg);
    return false;
  }
  return true;
}

void
tors_interfaces__srv__OrderMsg_Request__fini(tors_interfaces__srv__OrderMsg_Request * msg)
{
  if (!msg) {
    return;
  }
  // table_id
  // client_order_id
  rosidl_runtime_c__String__fini(&msg->client_order_id);
  // items_json
  rosidl_runtime_c__String__fini(&msg->items_json);
}

bool
tors_interfaces__srv__OrderMsg_Request__are_equal(const tors_interfaces__srv__OrderMsg_Request * lhs, const tors_interfaces__srv__OrderMsg_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // table_id
  if (lhs->table_id != rhs->table_id) {
    return false;
  }
  // client_order_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->client_order_id), &(rhs->client_order_id)))
  {
    return false;
  }
  // items_json
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->items_json), &(rhs->items_json)))
  {
    return false;
  }
  return true;
}

bool
tors_interfaces__srv__OrderMsg_Request__copy(
  const tors_interfaces__srv__OrderMsg_Request * input,
  tors_interfaces__srv__OrderMsg_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // table_id
  output->table_id = input->table_id;
  // client_order_id
  if (!rosidl_runtime_c__String__copy(
      &(input->client_order_id), &(output->client_order_id)))
  {
    return false;
  }
  // items_json
  if (!rosidl_runtime_c__String__copy(
      &(input->items_json), &(output->items_json)))
  {
    return false;
  }
  return true;
}

tors_interfaces__srv__OrderMsg_Request *
tors_interfaces__srv__OrderMsg_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tors_interfaces__srv__OrderMsg_Request * msg = (tors_interfaces__srv__OrderMsg_Request *)allocator.allocate(sizeof(tors_interfaces__srv__OrderMsg_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(tors_interfaces__srv__OrderMsg_Request));
  bool success = tors_interfaces__srv__OrderMsg_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
tors_interfaces__srv__OrderMsg_Request__destroy(tors_interfaces__srv__OrderMsg_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    tors_interfaces__srv__OrderMsg_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
tors_interfaces__srv__OrderMsg_Request__Sequence__init(tors_interfaces__srv__OrderMsg_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tors_interfaces__srv__OrderMsg_Request * data = NULL;

  if (size) {
    data = (tors_interfaces__srv__OrderMsg_Request *)allocator.zero_allocate(size, sizeof(tors_interfaces__srv__OrderMsg_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = tors_interfaces__srv__OrderMsg_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        tors_interfaces__srv__OrderMsg_Request__fini(&data[i - 1]);
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
tors_interfaces__srv__OrderMsg_Request__Sequence__fini(tors_interfaces__srv__OrderMsg_Request__Sequence * array)
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
      tors_interfaces__srv__OrderMsg_Request__fini(&array->data[i]);
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

tors_interfaces__srv__OrderMsg_Request__Sequence *
tors_interfaces__srv__OrderMsg_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tors_interfaces__srv__OrderMsg_Request__Sequence * array = (tors_interfaces__srv__OrderMsg_Request__Sequence *)allocator.allocate(sizeof(tors_interfaces__srv__OrderMsg_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = tors_interfaces__srv__OrderMsg_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
tors_interfaces__srv__OrderMsg_Request__Sequence__destroy(tors_interfaces__srv__OrderMsg_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    tors_interfaces__srv__OrderMsg_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
tors_interfaces__srv__OrderMsg_Request__Sequence__are_equal(const tors_interfaces__srv__OrderMsg_Request__Sequence * lhs, const tors_interfaces__srv__OrderMsg_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!tors_interfaces__srv__OrderMsg_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
tors_interfaces__srv__OrderMsg_Request__Sequence__copy(
  const tors_interfaces__srv__OrderMsg_Request__Sequence * input,
  tors_interfaces__srv__OrderMsg_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(tors_interfaces__srv__OrderMsg_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    tors_interfaces__srv__OrderMsg_Request * data =
      (tors_interfaces__srv__OrderMsg_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!tors_interfaces__srv__OrderMsg_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          tors_interfaces__srv__OrderMsg_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!tors_interfaces__srv__OrderMsg_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
tors_interfaces__srv__OrderMsg_Response__init(tors_interfaces__srv__OrderMsg_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    tors_interfaces__srv__OrderMsg_Response__fini(msg);
    return false;
  }
  return true;
}

void
tors_interfaces__srv__OrderMsg_Response__fini(tors_interfaces__srv__OrderMsg_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
tors_interfaces__srv__OrderMsg_Response__are_equal(const tors_interfaces__srv__OrderMsg_Response * lhs, const tors_interfaces__srv__OrderMsg_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
tors_interfaces__srv__OrderMsg_Response__copy(
  const tors_interfaces__srv__OrderMsg_Response * input,
  tors_interfaces__srv__OrderMsg_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

tors_interfaces__srv__OrderMsg_Response *
tors_interfaces__srv__OrderMsg_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tors_interfaces__srv__OrderMsg_Response * msg = (tors_interfaces__srv__OrderMsg_Response *)allocator.allocate(sizeof(tors_interfaces__srv__OrderMsg_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(tors_interfaces__srv__OrderMsg_Response));
  bool success = tors_interfaces__srv__OrderMsg_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
tors_interfaces__srv__OrderMsg_Response__destroy(tors_interfaces__srv__OrderMsg_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    tors_interfaces__srv__OrderMsg_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
tors_interfaces__srv__OrderMsg_Response__Sequence__init(tors_interfaces__srv__OrderMsg_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tors_interfaces__srv__OrderMsg_Response * data = NULL;

  if (size) {
    data = (tors_interfaces__srv__OrderMsg_Response *)allocator.zero_allocate(size, sizeof(tors_interfaces__srv__OrderMsg_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = tors_interfaces__srv__OrderMsg_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        tors_interfaces__srv__OrderMsg_Response__fini(&data[i - 1]);
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
tors_interfaces__srv__OrderMsg_Response__Sequence__fini(tors_interfaces__srv__OrderMsg_Response__Sequence * array)
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
      tors_interfaces__srv__OrderMsg_Response__fini(&array->data[i]);
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

tors_interfaces__srv__OrderMsg_Response__Sequence *
tors_interfaces__srv__OrderMsg_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tors_interfaces__srv__OrderMsg_Response__Sequence * array = (tors_interfaces__srv__OrderMsg_Response__Sequence *)allocator.allocate(sizeof(tors_interfaces__srv__OrderMsg_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = tors_interfaces__srv__OrderMsg_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
tors_interfaces__srv__OrderMsg_Response__Sequence__destroy(tors_interfaces__srv__OrderMsg_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    tors_interfaces__srv__OrderMsg_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
tors_interfaces__srv__OrderMsg_Response__Sequence__are_equal(const tors_interfaces__srv__OrderMsg_Response__Sequence * lhs, const tors_interfaces__srv__OrderMsg_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!tors_interfaces__srv__OrderMsg_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
tors_interfaces__srv__OrderMsg_Response__Sequence__copy(
  const tors_interfaces__srv__OrderMsg_Response__Sequence * input,
  tors_interfaces__srv__OrderMsg_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(tors_interfaces__srv__OrderMsg_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    tors_interfaces__srv__OrderMsg_Response * data =
      (tors_interfaces__srv__OrderMsg_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!tors_interfaces__srv__OrderMsg_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          tors_interfaces__srv__OrderMsg_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!tors_interfaces__srv__OrderMsg_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
