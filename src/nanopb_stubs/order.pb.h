/* Automatically generated nanopb header */
/* Generated by nanopb-0.4.2-dev */

#ifndef PB_WAVES_ORDER_PB_H_INCLUDED
#define PB_WAVES_ORDER_PB_H_INCLUDED
#include <pb.h>
#include "amount.pb.h"

#if PB_PROTO_HEADER_VERSION != 40
#error Regenerate this file with the current version of nanopb generator.
#endif

#ifdef __cplusplus
extern "C" {
#endif

/* Enum definitions */
typedef enum _waves_Order_Side {
    waves_Order_Side_BUY = 0,
    waves_Order_Side_SELL = 1
} waves_Order_Side;

/* Struct definitions */
typedef struct _waves_AssetPair {
    pb_callback_t amount_asset_id;
    pb_callback_t price_asset_id;
} waves_AssetPair;

typedef struct _waves_Order {
    int32_t chain_id;
    pb_callback_t sender_public_key;
    pb_callback_t matcher_public_key;
    bool has_asset_pair;
    waves_AssetPair asset_pair;
    waves_Order_Side order_side;
    int64_t amount;
    int64_t price;
    int64_t timestamp;
    int64_t expiration;
    bool has_matcher_fee;
    waves_Amount matcher_fee;
    int32_t version;
} waves_Order;


/* Helper constants for enums */
#define _waves_Order_Side_MIN waves_Order_Side_BUY
#define _waves_Order_Side_MAX waves_Order_Side_SELL
#define _waves_Order_Side_ARRAYSIZE ((waves_Order_Side)(waves_Order_Side_SELL+1))


/* Initializer values for message structs */
#define waves_AssetPair_init_default             {{{NULL}, NULL}, {{NULL}, NULL}}
#define waves_Order_init_default                 {0, {{NULL}, NULL}, {{NULL}, NULL}, false, waves_AssetPair_init_default, _waves_Order_Side_MIN, 0, 0, 0, 0, false, waves_Amount_init_default, 0}
#define waves_AssetPair_init_zero                {{{NULL}, NULL}, {{NULL}, NULL}}
#define waves_Order_init_zero                    {0, {{NULL}, NULL}, {{NULL}, NULL}, false, waves_AssetPair_init_zero, _waves_Order_Side_MIN, 0, 0, 0, 0, false, waves_Amount_init_zero, 0}

/* Field tags (for use in manual encoding/decoding) */
#define waves_AssetPair_amount_asset_id_tag      1
#define waves_AssetPair_price_asset_id_tag       2
#define waves_Order_chain_id_tag                 1
#define waves_Order_sender_public_key_tag        2
#define waves_Order_matcher_public_key_tag       3
#define waves_Order_asset_pair_tag               4
#define waves_Order_order_side_tag               5
#define waves_Order_amount_tag                   6
#define waves_Order_price_tag                    7
#define waves_Order_timestamp_tag                8
#define waves_Order_expiration_tag               9
#define waves_Order_matcher_fee_tag              10
#define waves_Order_version_tag                  11

/* Struct field encoding specification for nanopb */
#define waves_AssetPair_FIELDLIST(X, a) \
X(a, CALLBACK, SINGULAR, BYTES,    amount_asset_id,   1) \
X(a, CALLBACK, SINGULAR, BYTES,    price_asset_id,    2)
#define waves_AssetPair_CALLBACK pb_default_field_callback
#define waves_AssetPair_DEFAULT NULL

#define waves_Order_FIELDLIST(X, a) \
X(a, STATIC,   SINGULAR, INT32,    chain_id,          1) \
X(a, CALLBACK, SINGULAR, BYTES,    sender_public_key,   2) \
X(a, CALLBACK, SINGULAR, BYTES,    matcher_public_key,   3) \
X(a, STATIC,   OPTIONAL, MESSAGE,  asset_pair,        4) \
X(a, STATIC,   SINGULAR, UENUM,    order_side,        5) \
X(a, STATIC,   SINGULAR, INT64,    amount,            6) \
X(a, STATIC,   SINGULAR, INT64,    price,             7) \
X(a, STATIC,   SINGULAR, INT64,    timestamp,         8) \
X(a, STATIC,   SINGULAR, INT64,    expiration,        9) \
X(a, STATIC,   OPTIONAL, MESSAGE,  matcher_fee,      10) \
X(a, STATIC,   SINGULAR, INT32,    version,          11)
#define waves_Order_CALLBACK pb_default_field_callback
#define waves_Order_DEFAULT NULL
#define waves_Order_asset_pair_MSGTYPE waves_AssetPair
#define waves_Order_matcher_fee_MSGTYPE waves_Amount

extern const pb_msgdesc_t waves_AssetPair_msg;
extern const pb_msgdesc_t waves_Order_msg;

/* Defines for backwards compatibility with code written before nanopb-0.4.0 */
#define waves_AssetPair_fields &waves_AssetPair_msg
#define waves_Order_fields &waves_Order_msg

/* Maximum encoded size of messages (where known) */
/* waves_AssetPair_size depends on runtime parameters */
/* waves_Order_size depends on runtime parameters */

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif