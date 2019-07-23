package com.aim1.services;

import com.aim1.models.Movie;
import com.aim1.models.MovieDetail;
import com.aim1.models.MovieList;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

/**
 * Created by root on 18.01.18.
 */

public interface NiteoutService {

    @GET(UrlConstant.FETCH_MOVIES)
    Call<MovieList> fetchMovies();

    @GET(UrlConstant.FETCH_MOVIE_DETAIL)
    Call<MovieDetail> fetchMovieDetail(@Path("id") int id);
    //Rest of the services goes here

}
