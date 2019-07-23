package com.aim1.niteout;

import android.app.DatePickerDialog;
import android.app.TimePickerDialog;
import android.content.Context;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.TimePicker;

import com.aim1.adapters.MovieSpinnerAdapter;
import com.aim1.models.Movie;
import com.aim1.models.MovieDetail;
import com.aim1.models.MovieList;
import com.aim1.services.NiteoutService;
import com.aim1.services.NiteoutServiceFactory;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class Home extends AppCompatActivity implements DatePickerDialog.OnDateSetListener, TimePickerDialog.OnTimeSetListener {

    //Components
    private TextView _textViewDate;
    private TextView _textViewTime;
    private Spinner _moviesSpinner;

    //Data
    private List<Movie> _moviesList;
    private MovieSpinnerAdapter _movieSpinnerAdapter;
    private DatePicker _currentDatePicker;
    private TimePicker _currentTimePicker;
    private Movie _selectedMovie;
    private MovieDetail _selectedMovieDetail;
    private NiteoutService _service;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //Calling movies from server
        _service = NiteoutServiceFactory.getService();
        Call<MovieList> movies = _service.fetchMovies();
        movies.enqueue(new MovieCallback());

        setContentView(R.layout.activity_home);
        init();
    }

    private void init() {
        _textViewDate = findViewById(R.id.txtViewDate);
        _textViewTime = findViewById(R.id.txtViewTime);
        _moviesSpinner = findViewById(R.id.spinner);

        _textViewDate.setOnClickListener(view -> {
            DatePickerDialog datePickerDialog = new DatePickerDialog(Home.this, Home.this, 2018, 02,01);
            datePickerDialog.show();
        });
        _textViewTime.setOnClickListener(view -> {
            TimePickerDialog timePickerDialog = new TimePickerDialog(Home.this, Home.this, 0, 0,true);
            timePickerDialog.show();
        });

        _moviesList = new ArrayList<>();
        _movieSpinnerAdapter = new MovieSpinnerAdapter(this, _moviesList);
        _moviesSpinner.setAdapter(_movieSpinnerAdapter);
        _moviesSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                Movie selectedMovie = (Movie)   adapterView.getItemAtPosition(i);
                _selectedMovie = selectedMovie;
                Call<MovieDetail> movieDetail = _service.fetchMovieDetail(_selectedMovie.id);
                movieDetail.enqueue(new MovieDetailCallback());
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
                //do nothing
            }
        });
    }

    @Override
    public void onDateSet(DatePicker datePicker, int i, int i1, int i2) {
        String dateString = datePicker.getDayOfMonth() + "-" + (datePicker.getMonth()+1) + "-" + datePicker.getYear();
        _textViewDate.setText(dateString);
        _currentDatePicker = datePicker;
    }

    @Override
    public void onTimeSet(TimePicker timePicker, int i, int i1) {
        String timeString = timePicker.getHour() + ":" + timePicker.getMinute();
        _textViewTime.setText(timeString);
        _currentTimePicker = timePicker;
    }


    private class MovieCallback implements Callback<MovieList>{
        @Override
        public void onResponse(Call<MovieList> call, Response<MovieList> response) {
            if(response.isSuccessful()){
                MovieList movieList = response.body();
                _moviesList.clear();
                for(Movie movie: movieList.movies)
                    _moviesList.add(movie);
                _moviesList.forEach(movie ->
                        System.out.println(movie.id + ": " + movie.title)
                );
                _movieSpinnerAdapter.notifyDataSetChanged();
            } else{
                System.out.println(response.errorBody());
            }
        }

        @Override
        public void onFailure(Call<MovieList> call, Throwable t) {
            t.printStackTrace();
        }
    }

    private class MovieDetailCallback implements Callback<MovieDetail>{
        @Override
        public void onResponse(Call<MovieDetail> call, Response<MovieDetail> response) {
            if(response.isSuccessful()){
                Gson gson = new GsonBuilder().setPrettyPrinting().create();
                System.out.println(gson.toJson(response.body()));
                _selectedMovieDetail = response.body();
            } else{
                System.out.println(response.errorBody());
            }
        }

        @Override
        public void onFailure(Call<MovieDetail> call, Throwable t) {
            t.printStackTrace();
        }
    }
}
