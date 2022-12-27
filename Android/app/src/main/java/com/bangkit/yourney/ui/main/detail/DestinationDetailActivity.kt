package com.bangkit.yourney.ui.main.detail

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.constraintlayout.widget.ConstraintLayout
import com.bangkit.yourney.R
import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.data.sharedpreference.AuthPreference
import com.bangkit.yourney.data.sharedpreference.FavoriteDestinationPreference
import com.bangkit.yourney.databinding.ActivityDestinationDetailBinding
import com.bangkit.yourney.domain.model.Destination
import com.bangkit.yourney.ui.main.HomeActivity
import com.bangkit.yourney.ui.main.MainViewModel
import com.bangkit.yourney.utils.Constanta.DESTINATION_DATA
import com.bangkit.yourney.utils.GlobalUtils
import com.bangkit.yourney.utils.GlobalUtils.showToast
import com.bangkit.yourney.utils.ImageViewUtils.loadImageFromServer
import com.google.android.material.bottomsheet.BottomSheetBehavior
import com.google.android.material.bottomsheet.BottomSheetBehavior.BottomSheetCallback
import org.koin.androidx.viewmodel.ext.android.viewModel


class DestinationDetailActivity : AppCompatActivity() {
    private lateinit var binding: ActivityDestinationDetailBinding
    private val viewModel: MainViewModel by viewModel()
    private lateinit var mBottomSheetLayout: ConstraintLayout
    private lateinit var sheetBehavior: BottomSheetBehavior<*>
    private var isLiked = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityDestinationDetailBinding.inflate(layoutInflater)
        setContentView(binding.root)

        initBottomSheet()
        initViewData()
        binding.ivBack.setOnClickListener {
            finish()
        }
    }

    private fun initViewData() {
        val data = intent.getParcelableExtra<Destination>(DESTINATION_DATA)
        with(binding) {
            val pref = FavoriteDestinationPreference(this@DestinationDetailActivity)
//            if(pref.listFavoriteDestination().toString() == "null") {
//                setFavorite(false)
//            } else {
//                val currentData = pref.listFavoriteDestination()
//                for (item in currentData!!.indices) {
//                    if(currentData[item].idDestinasi == data!!.idDestinasi) {
//                        setFavorite(true)
//                        break
//                    }
//                    else if((currentData.size-1) == item) {
//                        setFavorite(false)
//                        break
//                    }
//                }
//            }
            val livedata = viewModel.checkFavorite(AuthPreference(this@DestinationDetailActivity).getToken, data?.idDestinasi.toString())
            livedata.observe(this@DestinationDetailActivity) { data ->
                if (data != null) {
                    when (data) {
                        is Resource.Loading<*> -> {
                            Log.d("TAG_LOADING", "JUST LOADING")
                        }
                        is Resource.Success<*> -> {
                            isLiked = data.data?.liked ?: false
                            setFavorite(isLiked)
                            livedata.removeObservers(this@DestinationDetailActivity)
                        }
                        is Resource.Error<*> -> {
                            setFavorite(false)
                            livedata.removeObservers(this@DestinationDetailActivity)
                        }
                    }
                }
            }
            ivBackgroundDestination.loadImageFromServer(data!!.picDestinasi)
            with(bottomSheetLayout) {
                tvDestinationName.text = data.namaDesinasi
                tvDestinationDesc.text = data.deskripsi
                tvLblTransport.text = "Transportation in ${data.namaDesinasi}"

                btnBookNow.setOnClickListener {
                    val intent =
                        Intent(Intent.ACTION_VIEW).setData(Uri.parse(data.urlDestinasi))
                    startActivity(intent)
                }
                ibFavorite.setOnClickListener {
                    if(isLiked) {
                        val likeLiveData = viewModel.removeFavorite(AuthPreference(this@DestinationDetailActivity).getToken, data.idDestinasi.toString())
                        likeLiveData.observe(this@DestinationDetailActivity) { data ->
                            if (data != null) {
                                when (data) {
                                    is Resource.Loading<*> -> {
                                        Log.d("TAG_LOADING", "JUST LOADING")
                                    }
                                    is Resource.Success<*> -> {
                                        isLiked = false
                                        setFavorite(isLiked)
                                        livedata.removeObservers(this@DestinationDetailActivity)
                                    }
                                    is Resource.Error<*> -> {
                                        setFavorite(false)
                                        livedata.removeObservers(this@DestinationDetailActivity)
                                    }
                                }
                            }
                        }
                    } else {
                        val likeLiveData = viewModel.addFavorite(AuthPreference(this@DestinationDetailActivity).getToken, data.idDestinasi.toString())
                        likeLiveData.observe(this@DestinationDetailActivity) { data ->
                            if (data != null) {
                                when (data) {
                                    is Resource.Loading<*> -> {
                                        Log.d("TAG_LOADING", "JUST LOADING")
                                    }
                                    is Resource.Success<*> -> {
                                        isLiked = true
                                        setFavorite(isLiked)
                                        livedata.removeObservers(this@DestinationDetailActivity)
                                    }
                                    is Resource.Error<*> -> {
                                        setFavorite(false)
                                        livedata.removeObservers(this@DestinationDetailActivity)
                                    }
                                }
                            }
                        }
                    }
                    if(pref.listFavoriteDestination().toString() == "null") {
                        val newData = ArrayList<Destination>()
                        newData.add(data)
                        pref.saveFavorite(newData)
                        setFavorite(true)
                    } else {
                        pref.listFavoriteDestination()!!.forEachIndexed { index, destinasi ->
                            if(destinasi.idDestinasi == data.idDestinasi) {
                                val newData = ArrayList<Destination>()
                                newData.addAll(pref.listFavoriteDestination()!!)
                                newData.removeAt(index)
                                pref.saveFavorite(newData)
                                showToast("Data has been remove from favorite!", this@DestinationDetailActivity)
                                setFavorite(false)
                            } else if(destinasi.idDestinasi != data.idDestinasi && index == (pref.listFavoriteDestination()!!.size - 1)) {
                                val newData = ArrayList<Destination>()
                                newData.addAll(pref.listFavoriteDestination()!!)
                                newData.add(data)
                                pref.saveFavorite(newData)
                                showToast("Data has been added to favorite!", this@DestinationDetailActivity)
                                setFavorite(true)
                            }
                        }
                    }
                }
            }
        }
    }

    private fun initBottomSheet() {
        mBottomSheetLayout = findViewById(R.id.bottom_sheet_layout)
        sheetBehavior = BottomSheetBehavior.from(mBottomSheetLayout)

        sheetBehavior.addBottomSheetCallback(object : BottomSheetCallback() {
            override fun onStateChanged(bottomSheet: View, newState: Int) {
                with(binding.bottomSheetLayout) {
                    if(sheetBehavior.state == BottomSheetBehavior.STATE_EXPANDED){
                        tvLblTransport.visibility = View.VISIBLE
                        layoutTransport.visibility = View.VISIBLE
                        layoutTransport2.visibility = View.VISIBLE
                    } else {
                        tvLblTransport.visibility = View.GONE
                        layoutTransport.visibility = View.GONE
                        layoutTransport2.visibility = View.GONE
                    }
                }
            }
            override fun onSlide(bottomSheet: View, slideOffset: Float) {}
        })
    }

    private fun setFavorite(state: Boolean) {
        binding.bottomSheetLayout.ibFavorite.setImageResource(if (state) R.drawable.ic_love_red else R.drawable.ic_love_grey)
    }
}