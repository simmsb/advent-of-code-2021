open Core

let day_name = "day1"

let day_input =
  let path =
    Fpath.(
      v (Sys.getcwd ()) / "aoc_inputs" / day_name |> set_ext "txt" |> to_string)
  in
  In_channel.read_lines path
  |> List.map ~f:(fun x -> String.strip x |> int_of_string)

let take_to l n t =
  let l2 = List.drop l n in
  List.take l2 t

let p1 =
  let len = List.length day_input - 1 in
  let l =
    List.map2_exn (take_to day_input 0 len) (take_to day_input 1 len)
      ~f:(fun a b ->
        if b > a then
          1
        else
          0)
  in
  List.sum (module Int) l ~f:(fun x -> x)

let p2 =
  let l = List.length day_input - 3 in
  let z = List.zip_exn (take_to day_input 0 l) (take_to day_input 3 l) in
  let l =
    List.map z ~f:(fun (a, b) ->
        if a < b then
          1
        else
          0)
  in
  List.sum (module Int) l ~f:(fun x -> x)

let () = Printf.printf "day 1: %d, day 2: %d" p1 p2
