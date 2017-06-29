<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreUser;
use App\User;
use App;
use File;

class ProspectiveController extends Controller
{
    public function index()
    {
        //dd('ProspectiveController');
        $path = resource_path().'/assets/json/Prospective.json';

        //dd($path);
        //dd(File::get($path));

         return response()->json(json_decode(File::get($path)));

        //$users = User::all();
        //return response()->json($users);
    }

    public function store(StoreUser $request)
    {
        $user = new User($request->all());
        $user->save();

        return response()->json($user);
    }
}
