#ifndef __UI_MENUS_NANOS_H__
#define __UI_MENUS_NANOS_H__

#include "os.h"
#include "cx.h"
#include "ux.h"

//////////////////////////////////////////////////////////////////////
UX_FLOW_DEF_NOCB(
    ux_idle_flow_1_step,
    bnn, //pnn,
    {
      "", //&C_icon_dashboard,
      "Application",
      "is ready",
    });
UX_FLOW_DEF_NOCB(
    ux_idle_flow_2_step,
    bn,
    {
      "Version",
      APPVERSION,
    });
UX_FLOW_DEF_VALID(
    ux_idle_flow_3_step,
    pb,
    os_sched_exit(-1),
    {
      &C_icon_dashboard,
      "Quit",
    });
const ux_flow_step_t *        const ux_idle_flow [] = {
  &ux_idle_flow_1_step,
  &ux_idle_flow_2_step,
  &ux_idle_flow_3_step,
  FLOW_END_STEP,
};

 //////////////////////////////////////////////////////////////////////
UX_FLOW_DEF_NOCB(
    ux_display_address_flow_1_step,
    pnn,
    {
      &C_icon_eye,
      "Verify",
      "address",
    });
UX_FLOW_DEF_NOCB(
    ux_display_address_flow_4_step,
    bnnn_paging,
    {
      .title = "Address",
      .text = fullAddress,
    });
UX_FLOW_DEF_VALID(
    ux_display_address_flow_5_step,
    pb,
    io_seproxyhal_touch_address_ok(NULL),
    {
      &C_icon_validate_14,
      "Approve",
    });
UX_FLOW_DEF_VALID(
    ux_display_address_flow_6_step,
    pb,
    io_seproxyhal_touch_address_cancel(NULL),
    {
      &C_icon_crossmark,
      "Reject",
    });


 const ux_flow_step_t *        const ux_display_address_flow [] = {
  &ux_display_address_flow_1_step,
  &ux_display_address_flow_4_step,
  &ux_display_address_flow_5_step,
  &ux_display_address_flow_6_step,
  FLOW_END_STEP,
};

 //////////////////////////////////////////////////////////////////////
UX_FLOW_DEF_NOCB(ux_approval_1_step,
    pnn,
    {
      &C_icon_eye,
      "Review",
      "transaction",
    });
UX_FLOW_DEF_NOCB(
    ux_approval_2_step,
    bnnn_paging,
    {
      .title = "Amount",
      .text = fullAmount,
    });
UX_FLOW_DEF_NOCB(
    ux_approval_3_step,
    bnnn_paging,
    {
      .title = "Address",
      .text = fullAddress,
    });
UX_FLOW_DEF_NOCB(
    ux_approval_4_step,
    bnnn_paging,
    {
      .title = "Source Tag",
      .text = tag,
    });
UX_FLOW_DEF_NOCB(
    ux_approval_5_step,
    bnnn_paging,
    {
      .title = "Destination Tag",
      .text = tag2,
    });
UX_FLOW_DEF_NOCB(
    ux_approval_6_step,
    bnnn_paging,
    {
      .title = "Fees",
      .text = maxFee,
    });
UX_FLOW_DEF_VALID(
    ux_approval_7_step,
    pbb,
    io_seproxyhal_touch_tx_ok(NULL),
    {
      &C_icon_validate_14,
      "Accept",
      "and send",
    });
UX_FLOW_DEF_VALID(
    ux_approval_8_step,
    pb,
    io_seproxyhal_touch_tx_cancel(NULL),
    {
      &C_icon_crossmark,
      "Reject",
    });
// confirm_full: confirm transaction / Amount: fullAmount / Address: fullAddress / Fees: feesAmount
// _xx: source tag || destination tag
const ux_flow_step_t *        const ux_approval_flow_11 [] = {
  &ux_approval_1_step,
  &ux_approval_2_step,
  &ux_approval_3_step,
  &ux_approval_4_step,
  &ux_approval_5_step,
  &ux_approval_6_step,
  &ux_approval_7_step,
  &ux_approval_8_step,
  FLOW_END_STEP,
};