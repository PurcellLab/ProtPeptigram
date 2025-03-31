=====
Usage
=====

To use ProtPeptigram in a project:

.. code-block:: python

    import ProtPeptigram

Basic Example
------------

Here's a simple example of how to use ProtPeptigram:

.. code-block:: python

    from ProtPeptigram import DataProcessor, viz
    
    # Load your protein or peptide data
    data = DataProcessor.load_data("path/to/your/data.csv")
    
    # Process the data
    processed_data = DataProcessor.process(data)
    
    # Visualize the results
    viz.plot(processed_data)

Advanced Usage
-------------

For more advanced usage examples, please refer to the :doc:`examples` section.