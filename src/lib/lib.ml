open Core

let day_input day_name =
  let path =
    Fpath.(
      v (Sys.getcwd ()) / "aoc_inputs" / day_name |> set_ext "txt" |> to_string)
  in
  In_channel.read_all path

let day_input_lines day_name =
  let path =
    Fpath.(
      v (Sys.getcwd ()) / "aoc_inputs" / day_name |> set_ext "txt" |> to_string)
  in
  In_channel.read_lines path
