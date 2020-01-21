workflow "build and ci" {
  on = "push"
  resolves = "test"
}
action "test" {
  uses = ./
}