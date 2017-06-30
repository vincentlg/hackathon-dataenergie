<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreUser;
use App\User;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;
use File;
use Illuminate\Http\Request;

class UserController extends Controller
{
    public function index()
    {
      $path = resource_path().'/assets/json/Users.json';
      return response()->json(json_decode(File::get($path)));
    }

    public function index_backup()
    {
      //todo fixe this dirty section !
      $process = new Process('sudo /root/anaconda3/envs/hack/bin/python /var/www/python/clustering_v1.py');
      $process->run();
      // executes after the command finishes
      if (!$process->isSuccessful()) {
          throw new ProcessFailedException($process);
      }

      $result = $process->getOutput();
      $clean = substr($result, 0, strlen($result)-1);
      return response()->json($clean);
    }

    public function store(Request $request)
    {

        $path = resource_path().'/assets/json/Users.json';
        $array = json_decode(File::get($path));
        //dd($array);
        $result = array_push($array, json_decode('{"lat":'.$request->input('lat').',"lng":'.$request->input('lng').'}'));
        File::put($path, json_encode($array));

        return response()->json(json_encode($array));
    }
}
