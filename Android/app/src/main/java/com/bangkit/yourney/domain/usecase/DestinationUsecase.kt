package com.bangkit.yourney.domain.usecase

import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.domain.model.Destination
import com.bangkit.yourney.domain.model.Favorite
import com.bangkit.yourney.domain.model.User
import kotlinx.coroutines.flow.Flow

interface DestinationUsecase {
    fun allDestination(token: String): Flow<Resource<List<Destination>>>
    fun filterDestination(token: String, filter: String): Flow<Resource<List<Destination>>>
    fun searchDestination(token: String, search: String): Flow<Resource<List<Destination>>>
    fun addFavorite(token: String, id: String): Flow<Resource<Favorite>>
    fun removeFavorite(token: String, id: String): Flow<Resource<Favorite>>
    fun checkFavorite(token: String, id: String): Flow<Resource<Favorite>>

}