from pystachio import (
  Default,
  Float,
  Integer,
  List,
  Map,
  Provided,
  Required,
  String,
  Struct
)

class ThermosContext(Struct):
  ports   = Map(String, Integer)
  task_id = String
  user    = String


# TODO(wickman)  Resource management/enforcement currently unsupported by Thermos
# and it's questionable whether it will ever be enforced or available in a standard
# way.  It could feasibly be enforced through some plugin mechanism perhaps.
class Resources(Struct):
  cpu  = Required(Float)
  ram  = Required(Integer)
  disk = Required(Integer)

  # TODO(wickman)  Add Boolean to pystachio
  best_effort = Default(Integer, 0)


class ProcessPair(Struct):
  first  = String
  second = String

class ProcessConstraint(Struct):
  ordered   = List(ProcessPair)

class Process(Struct):
  cmdline = Required(String)
  name    = Required(String)  # Making this required will make my life way easier.

  # optionals
  resources     = Resources
  daemon        = Default(Integer, 0)   # boolean, currently unsupported
  max_failures  = Default(Integer, 1)


@Provided(thermos = ThermosContext)
class Task(Struct):
  name      = Required(String)
  resources = Required(Resources)
  processes = List(Process)
  constraints = List(ProcessConstraint)

  max_failures  = Default(Integer, 1)
  min_successes = Default(Integer, 0)  # currently unsupported

  # 0 = infinite concurrency, > 0 => max concurrent processes.
  max_concurrency = Default(Integer, 0)

  user          = Default(String, '{{thermos.user}}')
