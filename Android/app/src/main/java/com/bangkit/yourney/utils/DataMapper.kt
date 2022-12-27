package com.bangkit.yourney.utils

import com.bangkit.yourney.data.source.remote.response.*
import com.bangkit.yourney.domain.model.Destination
import com.bangkit.yourney.domain.model.Favorite
import com.bangkit.yourney.domain.model.Upload
import com.bangkit.yourney.domain.model.User

object DataMapper {
    fun mapLoginResponseToDomain(input: ResponseLogin?, username: String) = User(
//        user_id = input?.user.user_id,
        username = input?.user?.username ?: username,
        email = input?.user?.email,
        avatar = input?.user?.userPic,
        status = input?.status,
        message = input?.message ?: "null",
        access = input?.access,
        refresh = input?.refresh,
    )

    fun mapRegisterResponseToDomain(input: ResponseRegister?) = User(
        username = input?.username,
        jenisKelamin = input?.jenisKelamin,
        tempatLahir = input?.tempatLahir,
        message = input?.message,
        status = input?.code
    )

    fun mapUserResponseToDomain(input: ResponseUser) = User(
        username = input.user?.username,
        full_name = input.user?.full_name,
        user_id = input.user?.id,
        avatar = input.user?.userPic,
        username_twitter = input.user?.usernameTwitter,
        tempatLahir = input.user?.tempatLahir,
        jenisKelamin = input.user?.jenisKelamin
    )

    fun mapUserDataResponseToDomain(input: UserData) = User(
        username = input.username,
        user_id = input.id,
        avatar = input.userPic,
        full_name = input.full_name,
        username_twitter = input.usernameTwitter,
        tempatLahir = input.tempatLahir,
        jenisKelamin = input.jenisKelamin
    )

    fun mapUploadeResponseToDomain(input: ResponseUpload) = Upload(
        status = input.status,
        url = input.url,
        message = input.message
    )

    fun mapFavoriteResponseToDomain(input: ResponseFavorite) = Favorite(
        liked = input.liked,
        message = input.message
    )

    fun mapDestinationResponseToDomain(input: ResponseDestination?) =
        input!!.responseDestination!!.map {
            Destination(
                namaDesinasi = it?.namaDesinasi,
                namaDestinasi = it?.namaDestinasi,
                idDestinasi = it?.idDestinasi,
                urlDestinasi = it?.urlDestinasi,
                picDestinasi = it?.picDestinasi,
                deskripsi = it?.deskripsi,
                idKategoriDestinasi = it?.idKategoriDestinasi
            )
        }

    fun mapListDestinationResponseToDomain(input: List<ResponseDestinationItem?>) =
        input.map {
            Destination(
                namaDesinasi = it?.namaDesinasi,
                namaDestinasi = it?.namaDestinasi,
                idDestinasi = it?.idDestinasi,
                urlDestinasi = it?.urlDestinasi,
                picDestinasi = it?.picDestinasi,
                deskripsi = it?.deskripsi,
                idKategoriDestinasi = it?.idKategoriDestinasi
            )
        }
}