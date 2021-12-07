open Core

module Tree = struct
  type t =
    | Node of (int * t) * (int * t)
    | Nil

  let rec insert t e =
    match e with
    | true :: xs -> (
      match t with
      | Node (n0, (c1, e1)) -> Node (n0, (succ c1, insert e1 xs))
      | Nil -> Node ((0, Nil), (1, insert Nil xs)))
    | false :: xs -> (
      match t with
      | Node ((c0, e0), n1) -> Node ((succ c0, insert e0 xs), n1)
      | Nil -> Node ((1, insert Nil xs), (0, Nil)))
    | [] -> Nil

  let build es = List.fold es ~init:Nil ~f:insert

  let find t ~f =
    let rec go t rs =
      match t with
      | Node (((_, e0) as n0), ((_, e1) as n1)) ->
        if f n0 n1 then
          go e1 (true :: rs)
        else
          go e0 (false :: rs)
      | Nil -> rs
    in
    go t []
end

let inp = Lib.day_input_lines "day3"

let ops =
  List.map inp ~f:(fun x ->
      String.to_list x
      |> List.map ~f:(function
           | '1' -> true
           | '0' -> false
           | c -> failwith (Printf.sprintf "bad input '%c'" c)))

let bool_list_to_int xs =
  List.foldi xs ~init:0 ~f:(fun i acc x -> acc lor (Bool.to_int x lsl i))

let part1 =
  let columns = List.transpose_exn ops in
  let most_common =
    List.map columns ~f:(fun l -> List.count l ~f:Fun.id > List.length l / 2)
    |> List.rev
  in
  let gamma = bool_list_to_int most_common in
  let epsilon = bool_list_to_int (List.map most_common ~f:not) in
  gamma * epsilon

let part2 =
  let tree = Tree.build ops in
  let o2 =
    Tree.find tree ~f:(fun (c0, _) (c1, _) ->
        match (c0, c1) with
        | 0, _ -> true
        | _, 0 -> false
        | _ -> c1 >= c0)
    |> bool_list_to_int
  in
  let co2 =
    Tree.find tree ~f:(fun (c0, _) (c1, _) ->
        match (c0, c1) with
        | 0, _ -> true
        | _, 0 -> false
        | _ -> c1 < c0)
    |> bool_list_to_int
  in
  o2 * co2

let () = Printf.printf "Part 1: %d\nPart 2: %d" part1 part2
