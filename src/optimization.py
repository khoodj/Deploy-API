from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyomo.environ import *
import random

app = FastAPI()


class Product(BaseModel):
    demand: int
    unit_profit: int


class OptimizationInput(BaseModel):
    num_products: int
    num_resources: int


def solve_optimization_problem(
    num_products: int,
    num_resources: int,
    products: list[Product],
    resource_capacity: list[int],
    resource_requirements: list[list[int]],
):
    # Create a concrete model
    model = ConcreteModel()

    # Define decision variables
    model.x = Var(range(num_products), within=NonNegativeIntegers)

    # Define objective function (maximize profit)
    model.obj = Objective(
        expr=sum(products[i].unit_profit * model.x[i] for i in range(num_products)),
        sense=maximize,
    )

    # Define demand constraints
    model.demand_constraints = ConstraintList()
    for i in range(num_products):
        model.demand_constraints.add(model.x[i] <= products[i].demand)

    # Define resource constraints
    model.resource_constraints = ConstraintList()
    for j in range(num_resources):
        model.resource_constraints.add(
            sum(resource_requirements[i][j] * model.x[i] for i in range(num_products))
            <= resource_capacity[j]
        )

    # Solve the optimization problem
    solver = SolverFactory("glpk")
    results = solver.solve(model)

    if str(results.solver.termination_condition) != "optimal":
        raise HTTPException(
            status_code=500, detail="Optimization problem could not be solved."
        )

    # Return production quantities for each product
    return [model.x[i].value for i in range(num_products)]


@app.post("/optimize/")
def optimize_production_plan(input_data: OptimizationInput):
    num_products = input_data.num_products
    num_resources = input_data.num_resources

    # Randomly generate resource capacity and product requirements
    resource_capacity = [
        random.randint(500, 1000) for _ in range(num_resources)
    ]  # Capacity of each resource
    resource_requirements = [
        [random.randint(5, 20) for _ in range(num_resources)]
        for _ in range(num_products)
    ]  # Resource requirements for each product

    # Randomly generate product demand and profit
    products = [
        Product(demand=random.randint(100, 200), unit_profit=random.randint(10, 20))
        for _ in range(num_products)
    ]

    # Solve the optimization problem
    production_quantities = solve_optimization_problem(
        num_products, num_resources, products, resource_capacity, resource_requirements
    )

    return {"production_quantities": production_quantities}
