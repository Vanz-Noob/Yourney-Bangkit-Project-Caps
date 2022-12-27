package com.bangkit.yourney.ui.main.home

import android.graphics.Bitmap
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.constraintlayout.widget.ConstraintSet
import androidx.recyclerview.widget.RecyclerView
import com.bangkit.yourney.R
import com.bangkit.yourney.databinding.ListItemDestinationBinding
import com.bangkit.yourney.domain.model.Destination
import com.bangkit.yourney.utils.GlideApp
import com.bumptech.glide.request.target.SimpleTarget
import com.bumptech.glide.request.transition.Transition

class DestinationListAdapter : RecyclerView.Adapter<DestinationListAdapter.ItemViewHolder>() {
    private var listData = ArrayList<Destination>()
    private lateinit var firstView: View
    private var firstViewPosition = 0
    private var isFirstTime = true

    var onItemClick: ((Destination) -> Unit)? = null
    var firstItem: ((View) -> Unit)? = null

    fun setData(newListData: List<Destination>?) {
        if (newListData == null) return
        listData.clear()
        listData.addAll(newListData)
        notifyDataSetChanged()
    }

    fun getPosition(): Int {
        return firstViewPosition
    }

    fun getFirstView(): View {
        return firstView
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        ItemViewHolder(
            LayoutInflater.from(parent.context)
                .inflate(R.layout.list_item_destination, parent, false)
        )

    override fun getItemCount() = listData.size

    override fun onBindViewHolder(holder: ItemViewHolder, position: Int) {
        val data = listData[position]
        if(!this::firstView.isInitialized) {
            firstView = holder.itemView
            firstViewPosition = position
        }
        holder.bind(data)
    }

    inner class ItemViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val binding = ListItemDestinationBinding.bind(itemView)
        private val set = ConstraintSet()
        fun bind(data: Destination) {
//            Log.d("TAG_CHECK", "${data.namaDesinasi} = $firstViewID")
            if(bindingAdapterPosition == firstViewPosition) {
                firstView = itemView
                if(isFirstTime) {
                    firstItem?.invoke(itemView)
                    isFirstTime = false
                }
            }
            with(binding) {
                textView2.text = data.namaDesinasi
                GlideApp.with(itemView.context)
                    .asBitmap()
                    .load(data.picDestinasi)
                    .into(object : SimpleTarget<Bitmap?>() {
                        override fun onResourceReady(
                            bitmap: Bitmap,
                            transition: Transition<in Bitmap?>?
                        ) {
                            val w = bitmap.width
                            val h = bitmap.height
                            imageView3.setImageBitmap(bitmap)
                            val ratio = String.format(
                                "%d:%d",
                                h,
                                w
                            )
                            set.clone(constraintLayout)
                            set.setDimensionRatio(imageView3.id, ratio)
                            set.applyTo(constraintLayout)
                        }
                    })
            }
        }

        init {
            binding.root.setOnClickListener {
                onItemClick?.invoke(listData[bindingAdapterPosition])
            }
        }
    }
}