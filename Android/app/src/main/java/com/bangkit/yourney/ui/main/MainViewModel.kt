package com.bangkit.yourney.ui.main

import androidx.lifecycle.ViewModel
import androidx.lifecycle.asLiveData
import com.bangkit.yourney.domain.usecase.AuthUsecase
import com.bangkit.yourney.domain.usecase.DestinationUsecase

class MainViewModel(private val useCase: DestinationUsecase) : ViewModel() {
    fun allDestination(token: String) = useCase.allDestination(token).asLiveData()
    fun filterDestination(token: String, filter: String) = useCase.filterDestination(token, filter).asLiveData()
    fun searchDestination(token: String, search: String) = useCase.searchDestination(token, search).asLiveData()
    fun checkFavorite(token: String, id: String) = useCase.checkFavorite(token, id).asLiveData()
    fun addFavorite(token: String, id: String) = useCase.addFavorite(token, id).asLiveData()
    fun removeFavorite(token: String, id: String) = useCase.removeFavorite(token, id).asLiveData()
}