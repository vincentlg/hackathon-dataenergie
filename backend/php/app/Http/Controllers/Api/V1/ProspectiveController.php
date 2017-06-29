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
      $path = resource_path().'/assets/json/Prospective.json';
      return response()->json(json_decode(File::get($path)));
    }
}
