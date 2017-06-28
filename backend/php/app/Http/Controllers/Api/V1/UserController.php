<?php

namespace App\Http\Controllers\Api\V1;

use App\Contracts\ResponseFormatter;
use App\Http\Controllers\Controller;
use App\Http\Requests\StoreUser;
use App\Models\User;
use App\Transformers\UserTransformer;

class UserController extends Controller
{
    private $transformer;
    private $response;


    public function index()
    {
        dd('hello');
        $users = User::all();

        return $this->response->responseCollection($users->all());
    }

    public function store(StoreUser $request)
    {
        $user = new User($request->all());
        $user->save();

        return $this->response->responseObject($this->transformer->transform($user));
    }

    public function show()
    {
        return $this->response->responseObject($this->transformer->transform(auth()->user()));
    }
}
