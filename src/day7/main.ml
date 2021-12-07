open Core

let inp =
  Lib.day_input "day7" |> String.strip |> String.split ~on:','
  |> List.map ~f:int_of_string

(* who doesn't love a little misapplied mathematics *)

let gradient_descent ~(bound : int * int) ~step ~limit ~f =
  let init = ((snd bound - fst bound) / 2) + fst bound |> Int.to_float
  and lower = fst bound |> Int.to_float
  and upper = snd bound |> Int.to_float
  and deriv x =
    let e = x +. 1.0 in
    (f e -. f x) /. 1.0
  in
  let next_step x =
    let next_x = x -. (step *. deriv x) in
    Float.clamp_exn next_x ~min:lower ~max:upper
  in
  let rec go x n =
    match n with
    | 0 -> x
    | n ->
      Printf.printf "%d: %f -> %f\n" n x (f x);
      let next_x = next_step x in
      if Float.to_int (f x) = Float.to_int (f next_x) then
        next_x
      else
        (go [@tailcall]) next_x (pred n)
  in
  go init limit

let list_int_min l = List.min_elt l ~compare:Int.compare |> Option.value_exn

let list_int_max l = List.max_elt l ~compare:Int.compare |> Option.value_exn

let day1 =
  let fuel_usage n =
    List.sum (module Float) inp ~f:(fun x -> Float.abs (Int.to_float x -. n))
  in
  let found_minima =
    gradient_descent
      ~bound:(list_int_min inp, list_int_max inp)
      ~step:0.5 ~limit:30 ~f:fuel_usage
  in
  [ -1.0; 0.0; 1.0 ]
  |> List.map ~f:(fun n -> fuel_usage (found_minima +. n) |> Float.to_int)
  |> list_int_min

let day2 =
  let tri n = n *. (n +. 1.0) /. 2.0 in
  let fuel_usage n =
    List.sum
      (module Float)
      inp
      ~f:(fun x -> Float.abs (Int.to_float x -. n) |> tri)
  in
  let found_minima =
    gradient_descent
      ~bound:(list_int_min inp, list_int_max inp)
      ~step:0.0005 ~limit:30 ~f:fuel_usage
  in
  [ -1.0; 0.0; 1.0 ]
  |> List.map ~f:(fun n -> fuel_usage (found_minima +. n) |> Float.to_int)
  |> list_int_min

let () = Printf.printf "Day 1: %d\nDay 2: %d\n" day1 day2
