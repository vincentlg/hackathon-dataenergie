<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreUser;
use App\User;

class UserController extends Controller
{
    public function index()
    {
        //dd('hello');
        $users = User::all();
        return response()->json($users);
    }

    public function store(StoreUser $request)
    {
        $user = new User($request->all());
        $user->save();

        return response()->json($user);
    }
}
