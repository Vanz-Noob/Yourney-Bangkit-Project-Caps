package com.bangkit.yourney.ui.user

import androidx.lifecycle.ViewModel
import androidx.lifecycle.asLiveData
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.domain.usecase.AuthUsecase
import com.bangkit.yourney.domain.usecase.DestinationUsecase
import com.bangkit.yourney.domain.usecase.UserUsecase
import java.io.File

class UserViewModel(private val useCase: UserUsecase) : ViewModel() {
    fun getUser(token: String) = useCase.getUser(token).asLiveData()
    fun updateUser(token: String, user: User) = useCase.updateUser(token, user).asLiveData()
    fun getFavorite(token: String) = useCase.getFavorite(token).asLiveData()
    fun uploadFile(token: String, file: File) = useCase.uploadFile(token, file).asLiveData()
}