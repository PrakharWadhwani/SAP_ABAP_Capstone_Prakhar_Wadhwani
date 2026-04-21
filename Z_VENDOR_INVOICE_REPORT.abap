*&---------------------------------------------------------------------*
*& Program     : Z_VENDOR_INVOICE_REPORT
*& Title       : Vendor Invoice ALV Report
*& Description : Custom ABAP ALV Report to display Vendor Invoice details
*&               fetched from SAP standard tables (LFA1, BSIK, BSAK)
*& Author      : PRAKHAR WADHWANI
*& Roll No     : 23053143
*& Branch      : BTECH/CSE
*& Date        : April 2026
*&---------------------------------------------------------------------*

REPORT z_vendor_invoice_report
  LINE-SIZE 255.

*----------------------------------------------------------------------*
* TYPE DECLARATIONS
*----------------------------------------------------------------------*
TYPES: BEGIN OF ty_vendor_invoice,
         bukrs    TYPE bukrs,
         lifnr    TYPE lifnr,
         name1    TYPE name1_gp,
         belnr    TYPE belnr_d,
         gjahr    TYPE gjahr,
         bldat    TYPE bldat,
         budat    TYPE budat,
         blart    TYPE blart,
         dmbtr    TYPE dmbtr,
         waers    TYPE waers,
         zterm    TYPE dzterm,
         zfbdt    TYPE dzfbdt,
         augdt    TYPE augdt,
         augbl    TYPE augbl,
         status   TYPE char15,
       END OF ty_vendor_invoice.

TYPES: ty_t_vendor_invoice TYPE STANDARD TABLE OF ty_vendor_invoice.

*----------------------------------------------------------------------*
* INTERNAL TABLES AND WORK AREAS
*----------------------------------------------------------------------*
DATA: gt_vendor_invoice TYPE ty_t_vendor_invoice,
      gs_vendor_invoice TYPE ty_vendor_invoice.

DATA: gt_fieldcat  TYPE slis_t_fieldcat_alv,
      gs_fieldcat  TYPE slis_fieldcat_alv,
      gs_layout    TYPE slis_layout_alv,
      gs_variant   TYPE disvariant,
      gt_sort      TYPE slis_t_sortinfo_alv,
      gs_sort      TYPE slis_sortinfo_alv.

*----------------------------------------------------------------------*
* SELECTION SCREEN
*----------------------------------------------------------------------*
SELECTION-SCREEN BEGIN OF BLOCK b1 WITH FRAME TITLE TEXT-001.
  SELECT-OPTIONS: s_bukrs FOR gs_vendor_invoice-bukrs OBLIGATORY,
                  s_lifnr FOR gs_vendor_invoice-lifnr,
                  s_bldat FOR gs_vendor_invoice-bldat,
                  s_budat FOR gs_vendor_invoice-budat,
                  s_gjahr FOR gs_vendor_invoice-gjahr.

  PARAMETERS: p_blart TYPE blart DEFAULT 'KR',
              p_open  TYPE char1 AS CHECKBOX DEFAULT 'X',
              p_clear TYPE char1 AS CHECKBOX DEFAULT 'X'.
SELECTION-SCREEN END OF BLOCK b1.

SELECTION-SCREEN BEGIN OF BLOCK b2 WITH FRAME TITLE TEXT-002.
  PARAMETERS: p_vari TYPE slis_vari.
SELECTION-SCREEN END OF BLOCK b2.

*----------------------------------------------------------------------*
* INITIALIZATION
*----------------------------------------------------------------------*
INITIALIZATION.
  TEXT-001 = 'Selection Criteria'.
  TEXT-002 = 'Display Variant'.

*----------------------------------------------------------------------*
* AT SELECTION-SCREEN ON VALUE-REQUEST
*----------------------------------------------------------------------*
AT SELECTION-SCREEN ON VALUE-REQUEST FOR p_vari.
  PERFORM f_get_variant.

*----------------------------------------------------------------------*
* START OF SELECTION
*----------------------------------------------------------------------*
START-OF-SELECTION.
  PERFORM f_get_data.
  PERFORM f_build_fieldcat.
  PERFORM f_set_layout.
  PERFORM f_set_sort.
  PERFORM f_display_alv.

*----------------------------------------------------------------------*
* FORM: F_GET_DATA
*----------------------------------------------------------------------*
FORM f_get_data.

  DATA: lt_bsik  TYPE STANDARD TABLE OF bsik,
        ls_bsik  TYPE bsik,
        lt_bsak  TYPE STANDARD TABLE OF bsak,
        ls_bsak  TYPE bsak,
        lt_lfa1  TYPE STANDARD TABLE OF lfa1,
        ls_lfa1  TYPE lfa1.

  " Fetch Open Items from BSIK
  IF p_open = 'X'.
    SELECT bukrs lifnr belnr gjahr bldat budat blart
           dmbtr waers zterm zfbdt
      FROM bsik
      INTO TABLE lt_bsik
     WHERE bukrs IN s_bukrs
       AND lifnr IN s_lifnr
       AND bldat IN s_bldat
       AND budat IN s_budat
       AND gjahr IN s_gjahr
       AND blart = p_blart.

    LOOP AT lt_bsik INTO ls_bsik.
      CLEAR gs_vendor_invoice.
      MOVE-CORRESPONDING ls_bsik TO gs_vendor_invoice.
      gs_vendor_invoice-status = 'Open'.
      APPEND gs_vendor_invoice TO gt_vendor_invoice.
    ENDLOOP.
  ENDIF.

  " Fetch Cleared Items from BSAK
  IF p_clear = 'X'.
    SELECT bukrs lifnr belnr gjahr bldat budat blart
           dmbtr waers zterm zfbdt augdt augbl
      FROM bsak
      INTO TABLE lt_bsak
     WHERE bukrs IN s_bukrs
       AND lifnr IN s_lifnr
       AND bldat IN s_bldat
       AND budat IN s_budat
       AND gjahr IN s_gjahr
       AND blart = p_blart.

    LOOP AT lt_bsak INTO ls_bsak.
      CLEAR gs_vendor_invoice.
      MOVE-CORRESPONDING ls_bsak TO gs_vendor_invoice.
      gs_vendor_invoice-status = 'Cleared'.
      APPEND gs_vendor_invoice TO gt_vendor_invoice.
    ENDLOOP.
  ENDIF.

  " Check if data exists
  IF gt_vendor_invoice IS INITIAL.
    MESSAGE 'No data found for the given selection criteria.' TYPE 'I'.
    LEAVE LIST-PROCESSING.
  ENDIF.

  " Fetch Vendor Names from LFA1
  SELECT lifnr name1
    FROM lfa1
    INTO TABLE lt_lfa1
     FOR ALL ENTRIES IN gt_vendor_invoice
   WHERE lifnr = gt_vendor_invoice-lifnr.

  " Enrich output table with vendor names
  LOOP AT gt_vendor_invoice INTO gs_vendor_invoice.
    READ TABLE lt_lfa1 INTO ls_lfa1
         WITH KEY lifnr = gs_vendor_invoice-lifnr.
    IF sy-subrc = 0.
      gs_vendor_invoice-name1 = ls_lfa1-name1.
      MODIFY gt_vendor_invoice FROM gs_vendor_invoice.
    ENDIF.
  ENDLOOP.

ENDFORM.

*----------------------------------------------------------------------*
* FORM: F_BUILD_FIELDCAT
*----------------------------------------------------------------------*
FORM f_build_fieldcat.

  DEFINE m_fieldcat.
    CLEAR gs_fieldcat.
    gs_fieldcat-fieldname   = &1.
    gs_fieldcat-seltext_m   = &2.
    gs_fieldcat-outputlen   = &3.
    gs_fieldcat-col_pos     = &4.
    gs_fieldcat-key         = &5.
    gs_fieldcat-do_sum      = &6.
    APPEND gs_fieldcat TO gt_fieldcat.
  END-OF-DEFINITION.

  m_fieldcat 'BUKRS'  'Company Code'     6    1  'X'  ' '.
  m_fieldcat 'LIFNR'  'Vendor No.'      10    2  'X'  ' '.
  m_fieldcat 'NAME1'  'Vendor Name'     30    3  ' '  ' '.
  m_fieldcat 'BELNR'  'Document No.'    10    4  ' '  ' '.
  m_fieldcat 'GJAHR'  'Fiscal Year'      4    5  ' '  ' '.
  m_fieldcat 'BLDAT'  'Doc. Date'       10    6  ' '  ' '.
  m_fieldcat 'BUDAT'  'Post. Date'      10    7  ' '  ' '.
  m_fieldcat 'BLART'  'Doc. Type'        2    8  ' '  ' '.
  m_fieldcat 'DMBTR'  'Amount (LC)'     15    9  ' '  'X'.
  m_fieldcat 'WAERS'  'Currency'         5   10  ' '  ' '.
  m_fieldcat 'ZTERM'  'Pay. Terms'       4   11  ' '  ' '.
  m_fieldcat 'ZFBDT'  'Baseline Date'   10   12  ' '  ' '.
  m_fieldcat 'AUGDT'  'Clearing Date'   10   13  ' '  ' '.
  m_fieldcat 'AUGBL'  'Clearing Doc.'   10   14  ' '  ' '.
  m_fieldcat 'STATUS' 'Status'          10   15  ' '  ' '.

ENDFORM.

*----------------------------------------------------------------------*
* FORM: F_SET_LAYOUT
*----------------------------------------------------------------------*
FORM f_set_layout.
  gs_layout-zebra             = 'X'.
  gs_layout-colwidth_optimize = 'X'.
  gs_layout-totals_text       = 'Grand Total'.
  gs_variant-report           = sy-repid.
  IF p_vari IS NOT INITIAL.
    gs_variant-variant = p_vari.
  ENDIF.
ENDFORM.

*----------------------------------------------------------------------*
* FORM: F_SET_SORT
*----------------------------------------------------------------------*
FORM f_set_sort.
  CLEAR gs_sort.
  gs_sort-fieldname = 'BUKRS'.
  gs_sort-spos      = 1.
  gs_sort-up        = 'X'.
  gs_sort-subtot    = 'X'.
  APPEND gs_sort TO gt_sort.

  CLEAR gs_sort.
  gs_sort-fieldname = 'LIFNR'.
  gs_sort-spos      = 2.
  gs_sort-up        = 'X'.
  gs_sort-subtot    = 'X'.
  APPEND gs_sort TO gt_sort.
ENDFORM.

*----------------------------------------------------------------------*
* FORM: F_DISPLAY_ALV
*----------------------------------------------------------------------*
FORM f_display_alv.
  CALL FUNCTION 'REUSE_ALV_GRID_DISPLAY'
    EXPORTING
      i_callback_program      = sy-repid
      i_callback_user_command = 'F_USER_COMMAND'
      it_fieldcat             = gt_fieldcat
      it_sort                 = gt_sort
      is_layout               = gs_layout
      is_variant              = gs_variant
      i_save                  = 'A'
      i_default               = 'X'
    TABLES
      t_outtab                = gt_vendor_invoice
    EXCEPTIONS
      program_error           = 1
      OTHERS                  = 2.

  IF sy-subrc <> 0.
    MESSAGE 'Error displaying ALV report.' TYPE 'E'.
  ENDIF.
ENDFORM.

*----------------------------------------------------------------------*
* FORM: F_USER_COMMAND  (Double-click -> Navigate to FB03)
*----------------------------------------------------------------------*
FORM f_user_command USING r_ucomm     TYPE sy-ucomm
                          rs_selfield TYPE slis_selfield.
  CASE r_ucomm.
    WHEN '&IC1'.
      READ TABLE gt_vendor_invoice INTO gs_vendor_invoice
           INDEX rs_selfield-tabindex.
      IF sy-subrc = 0.
        SET PARAMETER ID 'BUK' FIELD gs_vendor_invoice-bukrs.
        SET PARAMETER ID 'BLN' FIELD gs_vendor_invoice-belnr.
        SET PARAMETER ID 'GJR' FIELD gs_vendor_invoice-gjahr.
        CALL TRANSACTION 'FB03' AND SKIP FIRST SCREEN.
      ENDIF.
  ENDCASE.
ENDFORM.

*----------------------------------------------------------------------*
* FORM: F_GET_VARIANT
*----------------------------------------------------------------------*
FORM f_get_variant.
  DATA: ls_variant TYPE disvariant,
        lv_exit    TYPE char1.

  ls_variant-report = sy-repid.
  CALL FUNCTION 'REUSE_ALV_VARIANT_F4'
    EXPORTING
      is_variant = ls_variant
      i_save     = 'A'
    IMPORTING
      e_exit     = lv_exit
      es_variant = ls_variant
    EXCEPTIONS
      OTHERS     = 2.

  IF sy-subrc = 0 AND lv_exit IS INITIAL.
    p_vari = ls_variant-variant.
  ENDIF.
ENDFORM.

*&---------------------------------------------------------------------*
*& END OF PROGRAM: Z_VENDOR_INVOICE_REPORT
*&---------------------------------------------------------------------*
