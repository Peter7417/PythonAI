def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.
    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = float(1)

    for person in people:
        genes = (
            2 if person in two_genes else
            1 if person in one_gene else
            0
        )

        trait = person in have_trait
        mother = people[person]["mother"]
        father = people[person]["father"]

        # If person has no parents calculate unconditional probability
        if mother is None and father is None:
            probability *= PROBS["gene"][genes]

        # Otherwise calculate probabilities based on parents passing genes
        else:
            passing = {mother: 0, father: 0}

            for parent in passing:
                passing[parent] = (
                    # If the parent has two genes then it has 100% probability of passing unless it mutates
                    1 - PROBS["mutation"] if parent in two_genes else

                    # If the parent has only one gene then it has 50% probability of passing
                    0.5 if parent in one_gene else

                    # If the parent doesn't have a gene, the only way to get the gene is if it mutates
                    PROBS["mutation"]
                )

            probability *= (
                # Probability that both parents pass a gene
                passing[mother] * passing[father] if genes == 2 else

                # Probability of getting the gene from his mother and not his father or vice versa
                passing[mother] * (1 - passing[father]) + (1 - passing[mother]) * passing[father] if genes == 1 else

                # Probability of not getting the gene from any of the parents
                (1 - passing[mother]) * (1 - passing[father])
            )

        # Compute probability that a person does or does not have a particular trait
        probability *= PROBS["trait"][genes][trait]

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        genes = (
            2 if person in two_genes else
            1 if person in one_gene else
            0
        )

        trait = person in have_trait

        probabilities[person]["gene"][genes] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for field in probabilities[person]:
            total = sum(dict(probabilities[person][field]).values())
            for value in probabilities[person][field]:
                probabilities[person][field][value] /= total
