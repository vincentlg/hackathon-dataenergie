<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreUser;
use App\User;
use App;
use File;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class ClusteringController extends Controller
{
    public function index_old()
    {
      $path = resource_path().'/assets/json/Clustering.json';

      return response()->json(json_decode(File::get($path)));
    }
    public function index()
    {
      

      $process = new Process('/root/anaconda3/envs/hack/bin/python /var/www/python/clustering_v1.py');
      $process->run();

      // executes after the command finishes
      if (!$process->isSuccessful()) {
          throw new ProcessFailedException($process);
      }

      return response()->json($process->getOutput());

    }

    public function store(StoreUser $request)
    {
        $user = new User($request->all());
        $user->save();

        return response()->json($user);
    }
}
