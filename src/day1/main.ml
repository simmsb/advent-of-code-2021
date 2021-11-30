open Core

let day_name = "day1"

let day_input =
  let path =
    Fpath.(
      v (Sys.getcwd ()) / "aoc_inputs" / day_name |> set_ext "txt" |> to_string)
  in
  In_channel.read_lines path |> List.map ~f:String.strip

let () = Printf.printf "day1! %s\n" String.(concat ~sep:"\n" day_input)
