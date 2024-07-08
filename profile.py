"""A fully connected mesh using multiplexed best effort links. Since most nodes have a small number of
physical interfaces, we must set the links to use vlan ecapsulation over the physical link. On your
nodes, each one of the links will be implemented using a vlan network device. 

Instructions:
Log into your node, use `sudo` to poke around.
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Array of nodes
nodes = []

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

pc.defineParameter("N", "Number of nodes",
                   portal.ParameterType.INTEGER, 4)
pc.defineParameter("phystype",  "Optional physical node type (d710, etc)",
                   portal.ParameterType.STRING, "")
pc.defineParameter("data_size", "GPU node local storage size", portal.ParameterType.STRING, "1024GB")
pc.defineParameter("bestEffort",  "Best Effort", portal.ParameterType.BOOLEAN, True,
                    advanced=True,
                    longDescription="For very large lans, you might get an error saying 'not enough bandwidth.' " +
                    "This options tells the resource mapper to ignore bandwidth and assume you know what you " +
                    "are doing, just give me the lan I ask for (if enough nodes are available).")
pc.defineParameter("linkSpeed", "Link Speed",portal.ParameterType.INTEGER, 0,
                   [(0,"Any"),(100000,"100Mb/s"),(1000000,"1Gb/s"),(10000000,"10Gb/s"),(25000000,"25Gb/s"),(100000000,"100Gb/s")],
                   advanced=True,
                   longDescription="A specific link speed to use for your lan. Normally the resource " +
                   "mapper will choose for you based on node availability and the optional physical type.")
pc.defineParameter("tempFileSystemSize", "Temporary Filesystem Size",
                   portal.ParameterType.INTEGER, 0,advanced=True,
                   longDescription="The size in GB of a temporary file system to mount on each of your " +
                   "nodes. Temporary means that they are deleted when your experiment is terminated. " +
                   "The images provided by the system have small root partitions, so use this option " +
                   "if you expect you will need more space to build your software packages or store " +
                   "temporary files.")
pc.defineParameter("tempFileSystemMax",  "Temp Filesystem Max Space",
                    portal.ParameterType.BOOLEAN, True,
                    advanced=True,
                    longDescription="Instead of specifying a size for your temporary filesystem, " +
                    "check this box to allocate all available disk space. Leave the size above as zero.")

pc.defineParameter("tempFileSystemMount", "Temporary Filesystem Mount Point",
                   portal.ParameterType.STRING,"/data",advanced=True,
                   longDescription="Mount the temporary file system at this mount point; in general you " +
                   "you do not need to change this, but we provide the option just in case your software " +
                   "is finicky.")
params = pc.bindParameters()

# Create all the nodes.
for i in range(0, params.N):
    node = request.RawPC("node%d" % (i + 1))
    if params.phystype != "":
        node.hardware_type = params.phystype
        pass
    node.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'
    if params.tempFileSystemSize > 0 or params.tempFileSystemMax:
        bs = node.Blockstore("node%d" % (i + 1) + "-bs", params.tempFileSystemMount)
        if params.tempFileSystemMax:
            bs.size = "0GB"
        else:
            bs.size = str(params.tempFileSystemSize) + "GB"
            pass
        bs.placement = "any"
        pass    
    node.addService(rspec.Execute(shell="bash", command="/local/repository/setup_outside.sh"))
    #node.addService(rspec.Execute(shell="bash", command="/local/repository/setup_inside.sh"))
    nodes.append(node)
    pass

# Create all the links.
for i in range(0, params.N - 1):
    for j in range(i + 1, params.N):
        nodeA = nodes[i]
        nodeB = nodes[j]

        iface1 = nodeA.addInterface()
        iface2 = nodeB.addInterface()
        link   = request.Link()
        link.addInterface(iface1)
        link.addInterface(iface2)
        if params.bestEffort:
            link.best_effort = True
        elif params.linkSpeed > 0:
            link.bandwidth = params.linkSpeed
        link.link_multiplexing = True
        pass
    pass

pc.printRequestRSpec(request)
