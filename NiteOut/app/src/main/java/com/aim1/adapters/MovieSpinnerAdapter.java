package com.aim1.adapters;

import android.content.Context;
import android.support.annotation.NonNull;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.SpinnerAdapter;
import android.widget.TextView;

import com.aim1.models.Movie;
import com.aim1.niteout.R;

import java.util.List;

/**
 * Created by root on 19.01.18.
 */

public class MovieSpinnerAdapter extends BaseAdapter implements SpinnerAdapter{

    private Context _context;
    private List<Movie> _movies;

    public MovieSpinnerAdapter(Context context, List<Movie> movies){
        _context = context;
        _movies = movies;
    }

    @Override
    public int getCount() {
        return _movies.size();
    }

    @Override
    public Object getItem(int i) {
        return _movies.get(i);
    }

    @Override
    public long getItemId(int i) {
        return i;
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {
        TextView text;
        if (view != null){
            // Re-use the recycled view here!
            text = (TextView) view;
        } else {
            // No recycled view, inflate the "original" from the platform:
            LayoutInflater inflater = (LayoutInflater) _context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            text = (TextView) inflater.inflate(
                    android.R.layout.simple_dropdown_item_1line, viewGroup, false
            );
        }
        text.setText(_movies.get(i).title);
        return text;
    }
}
