package com.bangkit.yourney.ui.user

import android.Manifest
import android.app.Activity
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import android.webkit.MimeTypeMap
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.bangkit.yourney.R
import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.data.sharedpreference.AuthPreference
import com.bangkit.yourney.databinding.ActivityHomeBinding
import com.bangkit.yourney.databinding.ActivityUserSettingBinding
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.ui.authentication.AuthViewModel
import com.bangkit.yourney.ui.main.HomeActivity
import com.bangkit.yourney.utils.GlobalUtils
import com.bangkit.yourney.utils.GlobalUtils.showToast
import com.bangkit.yourney.utils.ImageViewUtils.loadImageFromLocal
import com.bangkit.yourney.utils.ImageViewUtils.loadImageFromServer
import com.bangkit.yourney.utils.ImageViewUtils.loadImageFromServerWithAuth
import com.bangkit.yourney.utils.ManagePermissions
import com.bumptech.glide.load.model.GlideUrl
import com.bumptech.glide.load.model.LazyHeaders
import com.github.dhaval2404.imagepicker.ImagePicker
import org.koin.androidx.viewmodel.ext.android.viewModel
import java.io.*

class UserSettingActivity : AppCompatActivity() {

    private lateinit var binding: ActivityUserSettingBinding
    private val viewModel: UserViewModel by viewModel()
    private val PermissionsRequestCode = 123
    private lateinit var managePermissions: ManagePermissions
    private var urlPic = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityUserSettingBinding.inflate(layoutInflater)
        setContentView(binding.root)
        init()
    }

    private fun init() {
        getUser()
        initClickAble()

        val list = listOf<String>(
            Manifest.permission.CAMERA,
            Manifest.permission.READ_EXTERNAL_STORAGE
        )

        // Initialize a new instance of ManagePermissions class
        managePermissions = ManagePermissions(this,list,PermissionsRequestCode)

        managePermissions.checkPermissions()
    }

    private fun initClickAble() {
        with(binding) {
            btnBack.setOnClickListener {
                finish()
            }
            btnSave.setOnClickListener {
                updateUser()
            }
            ibChangeProfile.setOnClickListener {
                ImagePicker.with(this@UserSettingActivity)
                    .crop()	    			//Crop image(Optional), Check Customization for more option
                    .compress(1024)			//Final image size will be less than 1 MB(Optional)
                    .maxResultSize(1080, 1080)	//Final image resolution will be less than 1080 x 1080(Optional)
                    .start()
            }
        }
    }

    private fun initView(data: User) {
        with(binding) {
                if(data.avatar == "null" || data.avatar == "" || data.avatar == null)
                    civImgAvatar.loadImageFromLocal(R.drawable.default_user_image)
                else
                    civImgAvatar.loadImageFromServer(data.avatar)
                tvHello.text = "Welcome ${data.username}"
                tietUsername.setText(data.full_name)
                tietUsernameDomicile.setText(data.tempatLahir)
                tietUsernameTwitter.setText(data.username_twitter)
                if(data.jenisKelamin == "L" || data.jenisKelamin == "Laki-laki" || data.jenisKelamin == "Laki-Laki" || data.jenisKelamin == "laki-laki") {
                    rbGenderMale.isChecked = true
                    rbGenderFemale.isChecked = false
                } else {
                    rbGenderMale.isChecked = false
                    rbGenderFemale.isChecked = true
                }
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode == Activity.RESULT_OK) {
            //Image Uri will not be null for RESULT_OK
            val uri: Uri = data?.data!!

            // Use Uri object instead of File to avoid storage permissions
            val livedata =
                viewModel.uploadFile(AuthPreference(this@UserSettingActivity).getToken, File(uri.path!!))
            livedata.observe(this) { upload ->
                if (upload != null) {
                    when (upload) {
                        is Resource.Loading<*> -> {
//                            myDialog.showCustomDialog(true)
                        }
                        is Resource.Success<*> -> {
                            binding.civImgAvatar.setImageURI(uri)
                            urlPic = (upload.data?.url ?: AuthPreference(this@UserSettingActivity).authData?.avatar)!!
                            livedata.removeObservers(this)
                        }
                        is Resource.Error<*> -> {
                            showToast(if(upload.message?.contains("{") == true)
                                GlobalUtils.getErrorMessageFromJSON(upload.message) else "UnExcepted Error",
                                this
                            )
                            viewState(isLoading = false, showView = true)
                            livedata.removeObservers(this)
                        }
                    }
                }
            }
        } else if (resultCode == ImagePicker.RESULT_ERROR) {
            showToast(ImagePicker.getError(data), this@UserSettingActivity)
        } else {
            showToast("Task Cancelled", this@UserSettingActivity)
        }
    }

    private fun getUser() {
        viewState(isLoading = true, showView = false)
        val livedata = viewModel.getUser(AuthPreference(this).getToken)
        livedata.observe(this) { data ->
            if (data != null) {
                when (data) {
                    is Resource.Loading<*> -> {
                        Log.d("TAG_LOADING", "JUST LOADING")
                    }
                    is Resource.Success<*> -> {
                        Log.d("TAG_DATA_S", data.data.toString())
                        Log.d("TAG_DATA_S", data.message.toString())
                        initView(data.data!!)
                        val accessBefore = AuthPreference(this@UserSettingActivity).authData
                        val user = data.data
                        user.access = accessBefore?.access
                        user.email = accessBefore?.email
                        user.refresh = accessBefore?.refresh
                        AuthPreference(this@UserSettingActivity).saveAuthData(user)
                        viewState(isLoading = false, showView = true)
                        livedata.removeObservers(this)
                    }
                    is Resource.Error<*> -> {
                        showToast(if(data.message?.contains("{") == true)
                            GlobalUtils.getErrorMessageFromJSON("data.message") else "UnExcepted Error",
                            this
                        )
                        viewState(isLoading = false, showView = true)
                        livedata.removeObservers(this)
                    }
                }
            }
        }
    }
    
    private fun updateUser() {
        viewState(isLoading = true, showView = false)
        with(binding) {
            val gender = if (rbGenderMale.isChecked)
                "L"
            else
                "P"
            val newData = User(
                full_name = tietUsername.text.toString(),
                username_twitter = tietUsernameTwitter.text.toString(),
                jenisKelamin = gender,
                tempatLahir = tietUsernameDomicile.text.toString(),
                avatar = if(urlPic == "") AuthPreference(this@UserSettingActivity).authData?.avatar else urlPic
            )

            val livedata = viewModel.updateUser(AuthPreference(this@UserSettingActivity).getToken, newData)
            livedata.observe(this@UserSettingActivity) { data ->
                if (data != null) {
                    when (data) {
                        is Resource.Loading<*> -> {
                            Log.d("TAG_LOADING", "JUST LOADING")
                        }
                        is Resource.Success<*> -> {
                            val accessBefore = AuthPreference(this@UserSettingActivity).authData
                            val user = data.data
                            user?.access = accessBefore?.access
                            user?.email = accessBefore?.email
                            user?.refresh = accessBefore?.refresh
                            AuthPreference(this@UserSettingActivity).saveAuthData(user)
                            initView(data.data!!)
                            viewState(isLoading = false, showView = true)
                            livedata.removeObservers(this@UserSettingActivity)
                        }
                        is Resource.Error<*> -> {
                            GlobalUtils.showToast(if(data.message?.contains("{") == true)
                                GlobalUtils.getErrorMessageFromJSON("data.message") else "UnExcepted Error",
                                this@UserSettingActivity
                            )
                            viewState(isLoading = false, showView = true)
                            livedata.removeObservers(this@UserSettingActivity)
                        }
                    }
                }
            }
        }
    }

    private fun viewState(showView: Boolean, isLoading:Boolean) {
        binding.mainLayout.visibility = if(showView) View.VISIBLE else View.GONE
        binding.viewLoading.loadingLayout.visibility = if(isLoading) View.VISIBLE else View.GONE
    }
}