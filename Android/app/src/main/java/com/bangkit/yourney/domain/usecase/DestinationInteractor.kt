package com.bangkit.yourney.domain.usecase

import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.domain.model.Destination
import com.bangkit.yourney.domain.model.Favorite
import com.bangkit.yourney.domain.repository.IAuthRepository
import com.bangkit.yourney.domain.repository.IDestinationRepository
import kotlinx.coroutines.flow.Flow

class DestinationInteractor(private val repository: IDestinationRepository) : DestinationUsecase {
    override fun allDestination(token: String): Flow<Resource<List<Destination>>> = repository.allDestination(token)
    override fun filterDestination(token: String, filter: String): Flow<Resource<List<Destination>>> = repository.filterDestination(token, filter)
    override fun searchDestination(token: String, search: String): Flow<Resource<List<Destination>>> = repository.searchDestination(token, search)
    override fun addFavorite(token: String, id: String): Flow<Resource<Favorite>> = repository.addFavorite(token, id)
    override fun removeFavorite(token: String, id: String): Flow<Resource<Favorite>> = repository.removeFavorite(token, id)
    override fun checkFavorite(token: String, id: String): Flow<Resource<Favorite>> = repository.checkFavorite(token, id)
}