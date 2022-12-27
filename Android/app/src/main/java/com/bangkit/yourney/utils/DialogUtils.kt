package com.bangkit.yourney.utils

import android.app.Dialog
import android.content.Context
import android.widget.ImageView
import android.widget.TextView

class DialogUtils {
    lateinit var dialog: Dialog

    fun showCustomDialog(
        context: Context,
        layoutID: Int
    ) {
        dialog = Dialog(context)
        dialog.setContentView(layoutID)
        dialog.setCanceledOnTouchOutside(true)
        dialog.create()
        dialog.show()
    }

    fun setCustomDialog(
        context: Context,
        layoutID: Int
    ) {
        dialog = Dialog(context)
        dialog.setContentView(layoutID)
        dialog.setCanceledOnTouchOutside(true)
        dialog.create()
    }

    fun showDialog() {
        dialog.show()
    }

    fun closeDialog() {
        dialog.dismiss()
    }
}