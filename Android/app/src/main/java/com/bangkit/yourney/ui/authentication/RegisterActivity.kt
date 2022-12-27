package com.bangkit.yourney.ui.authentication

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import com.bangkit.yourney.R
import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.data.sharedpreference.AuthPreference
import com.bangkit.yourney.data.source.remote.response.ResponseDefault
import com.bangkit.yourney.databinding.ActivityRegistrasiBinding
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.ui.main.HomeActivity
import com.bangkit.yourney.utils.DialogUtils
import com.bangkit.yourney.utils.GlobalUtils
import com.bangkit.yourney.utils.GlobalUtils.getErrorMessageFromJSON
import com.bangkit.yourney.utils.GlobalUtils.showToast
import com.google.gson.Gson
import org.koin.androidx.viewmodel.ext.android.viewModel

class RegisterActivity : AppCompatActivity() {
    private lateinit var binding: ActivityRegistrasiBinding
    private val viewModel: AuthViewModel by viewModel()
    private lateinit var dialogUtils: DialogUtils

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityRegistrasiBinding.inflate(layoutInflater)
        setContentView(binding.root)
        dialogUtils = DialogUtils()

        with(binding) {
            btnBack.setOnClickListener {
                finish()
            }
            btnRegister.setOnClickListener {
                processRegister()
            }
        }
    }

    private fun processRegister() {
        with(binding) {
            when {
                tietUsername.text.toString().isEmpty() -> {
                    tilUsername.error = "Required"
                }
                tietEmail.text.toString().isEmpty() -> {
                    tilEmail.error = "Required"
                }
                tietPassword.text.toString().isEmpty() -> {
                    tilPassword.error = "Required"
                }
                tietPlaceOfBirth.text.toString().isEmpty() -> {
                    tilPlaceOfBirth.error = "Required"
                }
                else -> {
                    viewState(showView = false, isLoading = true)
                    tietUsername.error = null
                    tietEmail.error = null
                    tietPassword.error = null
                    tietPlaceOfBirth.error = null
                    val gender = if (rbGenderMale.isChecked)
                        "L"
                    else
                        "P"
                    val user = User(
                        username = tietUsername.text.toString(),
                        password = tietPassword.text.toString(),
                        tempatLahir = tietPlaceOfBirth.text.toString(),
                        jenisKelamin = gender,
                        email = tietEmail.text.toString()
                    )

                    val livedata = viewModel.authRegister(user)
                    livedata.observe(this@RegisterActivity) { data ->
                        if (data != null) {
                            when (data) {
                                is Resource.Loading<*> -> {
                                    Log.d("TAG_LOADING", "JUST LOADING")
                                }
                                is Resource.Success<*> -> {
                                    livedata.removeObservers(this@RegisterActivity)
                                    viewState(showView = true, isLoading = false)
                                    Intent(this@RegisterActivity, LoginActivity::class.java).apply {
                                        startActivity(this)
                                    }
                                    finish()
                                }
                                is Resource.Error<*> -> {
                                    showToast(
                                        getErrorMessageFromJSON(data.message.toString()),
                                        this@RegisterActivity
                                    )
                                    viewState(showView = true, isLoading = false)
                                    livedata.removeObservers(this@RegisterActivity)
                                }
                            }
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