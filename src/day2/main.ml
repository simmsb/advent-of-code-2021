open Core

type opcode =
  | Down
  | Up
  | Forward

type operation =
  { opcode : opcode
  ; amount : int
  }

module Parser = struct
  open Angstrom

  let opcode =
    [ ("down", Down); ("up", Up); ("forward", Forward) ]
    |> List.map ~f:(fun (s, n) -> string s *> return n)
    |> choice

  let integer =
    take_while1 (function
      | '0' .. '9' -> true
      | _ -> false)
    >>| int_of_string

  let op =
    let open Let_syntax in
    let%bind op = opcode
    and _ = char ' '
    and amt = integer in
    return { opcode = op; amount = amt }
end

let inp = Lib.day_input_lines "day2"

let ops =
  List.map inp ~f:(fun x ->
      match Angstrom.parse_string ~consume:All Parser.op x with
      | Ok v -> v
      | Error msg -> failwith msg)

module type Solution = sig
  type t

  val init : t

  val perform : operation -> t -> t

  val extract : t -> int
end

let run_solution (type a) (module Solution : Solution with type t = a) ops =
  List.fold ops ~init:Solution.init ~f:(Fun.flip Solution.perform)
  |> Solution.extract

module Part1 : Solution = struct
  type t = int * int

  let init = (0, 0)

  let perform { opcode; amount } (x, y) =
    match opcode with
    | Forward -> (x + amount, y)
    | Down -> (x, y + amount)
    | Up -> (x, y - amount)

  let extract (x, y) = x * y
end

module Part2 : Solution = struct
  type t = int * int * int

  let init = (0, 0, 0)

  let perform { opcode; amount } (x, y, aim) =
    match opcode with
    | Forward -> (x + amount, y + (aim * amount), aim)
    | Down -> (x, y, aim + amount)
    | Up -> (x, y, aim - amount)

  let extract (x, y, _) = x * y
end

let () =
  let p1 = run_solution (module Part1) ops
  and p2 = run_solution (module Part2) ops in
  Printf.printf "Part 1: %d\nPart 2: %d\n" p1 p2
